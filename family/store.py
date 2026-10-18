from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get("FAMILY_DATA_DIR", ROOT / "data"))
KINDS = {"device", "person", "place", "preference", "routine", "delivery", "note"}


def now():
    return datetime.now(timezone.utc).isoformat()


def ident(prefix):
    return prefix + "_" + uuid.uuid4().hex[:12]


@contextmanager
def db():
    DATA.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATA / "family.db", timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def event(c, title, detail="", source="web", ref=None):
    c.execute("INSERT INTO events VALUES(?,?,?,?,?,?)", (ident("evt"), title, detail, source, ref, now()))


def init():
    with db() as c:
        c.executescript((Path(__file__).parent / 'schema.sql').read_text())
        if not c.execute("SELECT 1 FROM settings WHERE key='seeded'").fetchone():
            seed(c)
        from .demo import migrate_english_demo, migrate_callback
        migrate_english_demo(c)
        migrate_callback(c)


def seed(c):
    stamp = now()
    rows = [
        ("tv", "device", "Living-room TV", "DEMO DEVICE, not a real manufacturer's manual. Silver remote controls the TV; black remote controls the cable box. Cable box is connected to HDMI 1. For 'No signal': ask if there is text or a black screen; confirm the silver remote; ask caller to find the INPUT button by its label (position unknown); select HDMI 1 using arrows and OK; ask whether picture AND sound returned. Give ONE step at a time. If label is unreadable or no improvement, stop guessing and offer a family help request. Never diagnose internal faults or ask to open the TV."),
        ("channel", "preference", "Favorite channel", "Grandma explicitly prefers channel 67. This is a seeded test preference. Ask whether she wants that channel; do not assume every TV request means channel 67."),
        ("pickup", "place", "A Convenience Store", "DEMO pickup point: A Convenience Store at the village entrance. Opening hours and exact street address are unknown. Do not invent them."),
        ("rbc", "person", "Emma Hayes · Granddaughter", "Demo family contact. Receives help requests in the dashboard. No real destination phone number is configured; do not promise a phone call was made."),
        ("parcel", "delivery", "Rice cooker", json.dumps({"tracking_number":"DEMO-001", "carrier":"Demo carrier", "status":"in_transit", "pickup_place":"A Convenience Store", "pickup_code":None, "mode":"simulation", "last_checked":stamp}, ensure_ascii=False)),
        ("quiet", "routine", "Contact preferences", "Demo: use the dashboard for ordinary family follow-ups. Do not make outbound calls unless explicitly scheduled to the configured test recipient. No medication schedule is configured."),
    ]
    for key, kind, title, body in rows:
        c.execute("INSERT INTO records VALUES(?,?,?,?,?,?,1,?,?)", (key,kind,title,body,"seed",1,stamp,stamp))
    rid = ident("res")
    c.execute("INSERT INTO resources VALUES(?,?,?,?,?,?,?,?,?)", (rid,"Legacy fictional TV instruction card","text/plain",None,None,rows[0][3],"ready",None,stamp))
    for i, hours in enumerate((48,24)):
        cid = f"demo_call_{i}"
        ts = (datetime.now(timezone.utc)-timedelta(hours=hours)).isoformat()
        c.execute("INSERT INTO conversations VALUES(?,?,?,?,?,?,?,?)", (cid,"grandma","sample","ended","Sample: TV has no signal; family follow-up is needed.",1,ts,ts))
        c.execute("INSERT INTO messages(conversation_id,speaker,text,created_at) VALUES(?,?,?,?)",(cid,"caller","The television says no signal again.",ts))
    c.execute("INSERT INTO issues VALUES(?,?,?,?,?,?,?)",("issue_tv","tv","TV help keeps coming up","open","",stamp,stamp))
    for i in range(2):
        c.execute("INSERT INTO occurrences VALUES(?,?,?,?,?)",(ident("occ"),"issue_tv",f"demo_call_{i}","Sample: no signal reported; hardware failure is not established.",stamp))
    c.execute("INSERT INTO settings VALUES('seeded','true')")
    event(c,"Demo household prepared","Sample records and calls are labeled separately from real calls.","seed")


def all_records():
    with db() as c:
        return [dict(r) for r in c.execute("SELECT * FROM records ORDER BY updated_at DESC") if r["id"] not in setting("archived_record_ids",[])]


def apply_changes(changes, source, op_key=None):
    with db() as c:
        return apply_changes_in(c,changes,source,op_key)


def apply_changes_in(c, changes, source, op_key=None):
    if not changes or len(changes)>12:
        raise ValueError("Provide between 1 and 12 changes.")
    if op_key:
        old = c.execute("SELECT result FROM operations WHERE key=?",(op_key,)).fetchone()
        if old:
            return json.loads(old[0])
    result=[]
    for change in changes:
        kind, title, body = (str(change.get(k,"")).strip() for k in ("kind","title","body"))
        if kind not in KINDS or not title or not body or len(title)>180 or len(body)>60000:
            raise ValueError("Check the record category, title and content.")
        rid=change.get("record_id")
        if rid and rid!="new":
            archive=c.execute("SELECT value FROM settings WHERE key='archived_record_ids'").fetchone()
            if archive and rid in json.loads(archive[0]):
                raise ValueError('This record is archived. Create a fresh handover instead.')
            old=c.execute("SELECT * FROM records WHERE id=?",(rid,)).fetchone()
            if not old:
                raise ValueError("The record was not found. Reload the family information.")
            if change.get("expected_version") is not None and old["version"]!=change["expected_version"]:
                raise ValueError("This record changed elsewhere. Reopen it before editing.")
            if old["kind"]=="delivery":
                raise ValueError("Use parcel actions to update delivery status.")
            c.execute("UPDATE records SET kind=?,title=?,body=?,source=?,version=version+1,updated_at=? WHERE id=?",(kind,title,body,source,now(),rid))
            verb="Information updated"
        else:
            if kind=="delivery":
                raise ValueError("Adding live parcels is not available in this demo.")
            rid=ident("rec")
            c.execute("INSERT INTO records VALUES(?,?,?,?,?,0,1,?,?)",(rid,kind,title,body,source,now(),now()))
            verb="Information saved"
        event(c,verb,title,source,rid)
        result.append(rid)
    if op_key:
        c.execute("INSERT INTO operations VALUES(?,?)",(op_key,json.dumps(result)))
    return result


def start_conversation(cid, role="unknown", channel="phone", demo=False):
    with db() as c:
        c.execute("INSERT OR IGNORE INTO conversations VALUES(?,?,?,?,?,?,?,NULL)",(cid,role,channel,"active","",int(demo),now()))


def message(cid, speaker, text, utterance_id=None):
    with db() as c:
        c.execute("INSERT INTO messages(conversation_id,speaker,text,utterance_id,created_at) VALUES(?,?,?,?,?) ON CONFLICT(conversation_id,utterance_id) DO UPDATE SET text=excluded.text",(cid,speaker,text,utterance_id,now()))


def conversation(cid):
    with db() as c:
        row=c.execute("SELECT * FROM conversations WHERE id=?",(cid,)).fetchone()
        if not row:
            raise ValueError("Conversation not found.")
        return {**dict(row),"messages":[dict(m) for m in c.execute("SELECT * FROM messages WHERE conversation_id=? ORDER BY id",(cid,))]}


def add_issue(cid, topic, title, evidence):
    with db() as c:
        old=c.execute("SELECT id FROM issues WHERE topic=? AND status!='resolved' ORDER BY created_at DESC LIMIT 1",(topic,)).fetchone()
        issue_id=old[0] if old else ident("issue")
        if not old:
            c.execute("INSERT INTO issues VALUES(?,?,?,?,?,?,?)",(issue_id,topic,title,"open","",now(),now()))
        c.execute("INSERT INTO occurrences VALUES(?,?,?,?,?) ON CONFLICT(issue_id,conversation_id) DO UPDATE SET evidence=excluded.evidence",(ident("occ"),issue_id,cid,evidence[:5000],now()))
        c.execute("UPDATE issues SET updated_at=? WHERE id=?",(now(),issue_id))
        return issue_id


def set_issue(issue_id, status, owner=""):
    if status not in {"open","claimed","resolved"}:
        raise ValueError("Invalid follow-up status.")
    with db() as c:
        if not c.execute("UPDATE issues SET status=?,owner=?,updated_at=? WHERE id=?",(status,owner[:100],now(),issue_id)).rowcount:
            raise ValueError("Follow-up not found.")
        event(c,"Follow-up updated",status,"web",issue_id)


def end_conversation(cid, summary=""):
    with db() as c:
        c.execute("UPDATE conversations SET state='ended',ended_at=?,summary=? WHERE id=?",(now(),summary[:3000],cid))


def setting(key, default=None):
    with db() as c:
        r=c.execute("SELECT value FROM settings WHERE key=?",(key,)).fetchone()
        return json.loads(r[0]) if r else default


def put_setting(key, value):
    with db() as c:
        c.execute("INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(key,json.dumps(value)))


def snapshot():
    with db() as c:
        return {
          "records":all_records(),
          "resources":[dict(r) for r in c.execute("SELECT id,title,mime,url,status,error,created_at,(SELECT conversation_id FROM conversation_resources WHERE resource_id=resources.id LIMIT 1) conversation_id FROM resources WHERE status!='archived' ORDER BY created_at DESC")],
          "conversations":[dict(r) for r in c.execute("SELECT c.*, co.outcome, (SELECT COUNT(*) FROM messages m WHERE m.conversation_id=c.id) message_count FROM conversations c LEFT JOIN call_outcomes co ON co.conversation_id=c.id ORDER BY started_at DESC LIMIT 80") if r["id"] not in setting("archived_conversation_ids",[])],
          "issues":[dict(r) for r in c.execute("SELECT i.*, COUNT(o.id) occurrences, SUM(CASE WHEN o.conversation_id IN (SELECT id FROM conversations WHERE demo=0) THEN 1 ELSE 0 END) real_occurrences, (SELECT evidence FROM occurrences WHERE issue_id=i.id ORDER BY created_at DESC LIMIT 1) latest_evidence FROM issues i LEFT JOIN occurrences o ON o.issue_id=i.id GROUP BY i.id ORDER BY CASE i.status WHEN 'open' THEN 0 WHEN 'claimed' THEN 1 ELSE 2 END, i.updated_at DESC")],
          "jobs":[dict(r) for r in c.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT 40")],
          "events":[dict(r) for r in c.execute("SELECT * FROM events ORDER BY created_at DESC LIMIT 35")],
          "phone":setting("phone_status",{"state":"offline"}),
          "updated_at":now(),
        }


def context(query=""):
    # Lightweight retrieval for the local prototype; no vector-store service required.
    with db() as c:
        resources=[dict(r) for r in c.execute("SELECT id,title,text,status FROM resources WHERE status='ready' ORDER BY created_at DESC")]
        tasks=[dict(r) for r in c.execute("SELECT id,title,due_at,status,mode,result FROM jobs ORDER BY created_at DESC LIMIT 30")]
    with db() as c:
        followups=[dict(r) for r in c.execute("SELECT i.title,i.status,i.owner,n.text note FROM issues i LEFT JOIN issue_notes n ON n.issue_id=i.id ORDER BY n.created_at DESC LIMIT 10")]
    terms=set(re.findall(r"[a-z0-9]{2,}",query.lower()))-{"the","what","where","how","does","can","you","with","and","for","that","this","please","my"}
    for part in re.findall(r"[\u4e00-\u9fff]+",query):
        terms.update(part[i:i+2] for i in range(len(part)-1))
    candidates=[]
    for resource in resources:
        for offset in range(0,len(resource['text']),1800):
            chunk=resource['text'][offset:offset+2200]
            score=sum((chunk.lower().count(t)+2*resource['title'].lower().count(t)) for t in terms)
            candidates.append((score,{"resource_id":resource['id'],"title":resource['title'],"offset":offset,"text":chunk}))
    candidates.sort(key=lambda pair:pair[0],reverse=True)
    selected=[chunk for _,chunk in candidates[:8]]
    records=[{**r,"body":r['body'][:12000],"excerpted":len(r['body'])>12000} for r in all_records()]
    return json.dumps({"household_profile":setting("family_profile",{}),"records":records,"tasks":tasks,"family_followups":followups,"resource_excerpts":selected,"retrieval":{"method":"keyword-ranked excerpts","total_chunks":len(candidates),"returned_chunks":len(selected),"instruction":"Excerpts are not the full documents. If the needed fact is absent, ask the caller a focused question to clarify it."}},ensure_ascii=False)


def add_job(title, payload, due_at, mode="dashboard", dedup=None):
    date=datetime.fromisoformat(due_at.replace("Z","+00:00"))
    if date.tzinfo is None:
        raise ValueError("Reminder time must include a timezone.")
    if mode not in {"dashboard","phone"}:
        raise ValueError("Invalid reminder method.")
    with db() as c:
        jid=ident("job")
        c.execute("INSERT OR IGNORE INTO jobs VALUES(?,?,?,?,?,?,?,0,'',?)",(jid,title,json.dumps(payload,ensure_ascii=False),date.astimezone(timezone.utc).isoformat(),"pending",mode,dedup,now()))
        row=c.execute("SELECT id FROM jobs WHERE dedup_key=?",(dedup,)).fetchone() if dedup else None
        return row[0] if row else jid


def parcel_status(record_id, status, source="simulation"):
    if status not in {"in_transit","ready_for_pickup","collected"}:
        raise ValueError("Invalid parcel status.")
    with db() as c:
        r=c.execute("SELECT * FROM records WHERE id=? AND kind='delivery'",(record_id,)).fetchone()
        if not r:
            raise ValueError("Parcel not found.")
        p=json.loads(r["body"])
        if source=="simulation" and p.get("mode")!="simulation":
            raise ValueError("Simulated events are only allowed for demo parcels.")
        previous=p["status"]
        p.update(status=status,last_checked=now())
        c.execute("UPDATE records SET body=?,updated_at=?,version=version+1,source=? WHERE id=?",(json.dumps(p,ensure_ascii=False),now(),source,record_id))
        if status=="collected":
            c.execute("UPDATE jobs SET status='cancelled',result='Caller reported parcel collected' WHERE dedup_key=? AND status='pending'",(f"parcel:{record_id}:ready",))
        if previous!=status:
            event(c,"Parcel status updated",f"{r['title']} → {status}",source,record_id)
    if status=="ready_for_pickup":
        add_job("Pickup reminder · "+r["title"],{"message":f"{r['title']} is ready for pickup at {p.get('pickup_place','location unknown')}. Pickup code: {p.get('pickup_code') or 'not provided'}. This is demo logistics data."},now(),dedup=f"parcel:{record_id}:ready")
