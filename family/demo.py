"""A fictional household with a real, attributed photo and sourced operating facts."""
import json
from pathlib import Path
from . import store

ASSETS=Path(__file__).parent/'static'/'demo'
PHOTO_SOURCE='https://commons.wikimedia.org/wiki/File:A_Roku_TV_Remote.jpg'
REMOTE_GUIDE='https://support.roku.com/en-au/article/simple-remote-setup'
NETFLIX_GUIDE='https://help.netflix.com/en/node/23886/'
DEFAULT_PROFILE={
    'household_name':"June's circle", 'member_name':'Emma Hayes', 'relationship':'Granddaughter',
    'elder_name':'June Hayes', 'elder_call_name':'June', 'backup_name':'Daniel Hayes',
    'backup_relationship':'Son', 'timezone':'America/Los_Angeles', 'language':'English',
    'sharing_acknowledged':False, 'onboarded':False,
}
HOUSEHOLD_NOTE='''June uses a television with a Roku streaming player. The black Roku remote has a purple directional pad with OK in the middle. It is kept in the woven basket beside her armchair.
The white Netflix button has red lettering. It is below the playback buttons and to the left of Disney+. The house-shaped Home button is at the top right.
Emma installed Netflix and signed in during setup. June would like help opening Netflix. The TV also has a separate remote.
Emma Hayes is the primary family contact for follow-ups in the dashboard. Daniel Hayes is the backup.
'''
SOURCE_NOTE='''# Roku remote: reference notes

The pictured remote has a black body, a purple directional pad with OK, a house-shaped Home button at the top right, and a white Netflix key with red letters below the playback buttons, to the left of Disney+.

Roku's simple-remote guide describes infrared communication: point the remote toward the Roku device with a clear path. App shortcut buttons open their named streaming apps.
Source: https://support.roku.com/en-au/article/simple-remote-setup

Netflix provides instructions for using Netflix on Roku. Installation and sign-in are part of household setup.
Source: https://help.netflix.com/en/node/23886/

Photo: A Roku TV Remote, Texas Lane, 21 June 2022. Original photograph, unchanged. CC BY-SA 4.0.
Source: https://commons.wikimedia.org/wiki/File:A_Roku_TV_Remote.jpg
License: https://creativecommons.org/licenses/by-sa/4.0/
'''



def profile():
    return {**DEFAULT_PROFILE,**store.setting('family_profile',{})}


def save_profile(data):
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    try: ZoneInfo(data['timezone'])
    except (ZoneInfoNotFoundError,ValueError): raise ValueError('Choose a valid timezone.') from None
    if not data.get('sharing_acknowledged'):
        raise ValueError('Confirm the sharing arrangement before continuing.')
    data={k:v.strip() if isinstance(v,str) else v for k,v in data.items()}
    for key in ('household_name','member_name','relationship','elder_name','elder_call_name','backup_name'):
        if not data.get(key): raise ValueError('Complete the household names and relationships.')
    data.update(language='English',onboarded=True)
    store.put_setting('family_profile',data)
    with store.db() as c:
        c.execute("UPDATE records SET title=?,body=?,source='onboarding',version=version+1,updated_at=? WHERE id='rbc'",(data['member_name']+' · '+data['relationship'],data['member_name']+' is the primary dashboard contact. '+data['backup_name']+' is the backup. Follow-ups are shared in the family dashboard.',store.now()))
        store.event(c,'Family circle updated',f"{data['member_name']} supports {data['elder_call_name']}; {data['backup_name']} is the backup.",'onboarding')
    return data


def prepare_files():
    ASSETS.mkdir(parents=True,exist_ok=True)
    (ASSETS/'household-note.txt').write_text(HOUSEHOLD_NOTE)
    (ASSETS/'source-notes.md').write_text(SOURCE_NOTE)


def setup_status():
    with store.db() as c:
        photo=c.execute("SELECT id,status FROM resources WHERE title='roku-tv-remote.jpg' AND status!='archived' ORDER BY CASE status WHEN 'ready' THEN 0 ELSE 1 END, created_at DESC LIMIT 1").fetchone()
        guide=c.execute("SELECT id,status FROM resources WHERE title='source-notes.md' AND status!='archived' ORDER BY CASE status WHEN 'ready' THEN 0 ELSE 1 END, created_at DESC LIMIT 1").fetchone()
    notes=any('roku' in r['body'].lower() and 'netflix' in r['body'].lower() for r in store.all_records())
    return {'photo':dict(photo) if photo else None,'guide':dict(guide) if guide else None,'household_notes':notes,
            'household_message':HOUSEHOLD_NOTE,'photo_source':PHOTO_SOURCE,'remote_guide':REMOTE_GUIDE,'netflix_guide':NETFLIX_GUIDE}


def migrate_english_demo(c):
    # Recover uploads made before the conversation-based interface existed.
    orphans=c.execute("SELECT id,title FROM resources WHERE status NOT IN ('ready','archived') AND id NOT IN (SELECT resource_id FROM conversation_resources)").fetchall()
    for r in orphans:
        cid=store.ident('chat')
        c.execute("INSERT INTO conversations VALUES(?,'family','web','active','',0,?,NULL)",(cid,store.now()))
        c.execute('INSERT INTO conversation_resources VALUES(?,?)',(cid,r['id']))
        c.execute("INSERT INTO messages(conversation_id,speaker,text,created_at) VALUES(?,'system',?,?)",(cid,'This file was uploaded in the earlier interface. Continue the handover here; its contents are not yet shared with calls.',store.now()))
    c.execute("UPDATE issues SET owner='Family member' WHERE owner='家人'")
    if c.execute("SELECT 1 FROM settings WHERE key='english_demo_v2'").fetchone(): return
    # Retire earlier fictional device instructions so they cannot conflict with the new photo.
    archived=['tv']
    for r in c.execute('SELECT id,title FROM records'):
        if r['title'] in {'测试 · 卧室台灯','测试笔记 · 橙色手电筒位置'}: archived.append(r['id'])
    c.execute("INSERT OR REPLACE INTO settings VALUES('archived_record_ids',?)",(json.dumps(archived),))
    c.execute("UPDATE resources SET status='archived' WHERE title IN ('demo-remote.png','bedside-lamp.md','示例：电视操作卡（虚构）','Legacy fictional TV instruction card')")
    translations=json.loads((Path(__file__).parent/'legacy_labels.json').read_text())
    # Translate application-authored labels. Raw caller messages are never rewritten.
    for table,columns in {'records':['title'],'issues':['title','owner'],'events':['title','detail'],'jobs':['title','result']}.items():
        for row in c.execute(f'SELECT * FROM {table}').fetchall():
            for col in columns:
                value=row[col] or ''
                for a,b in sorted(translations.items(),key=lambda x:-len(x[0])): value=value.replace(a,b)
                if value!=row[col]: c.execute(f'UPDATE {table} SET {col}=? WHERE id=?',(value,row['id']))
    old_chats=[r[0] for r in c.execute("SELECT DISTINCT c.id FROM conversations c JOIN messages m ON m.conversation_id=c.id WHERE c.channel='web' AND (m.text LIKE '%橙色手电筒%' OR m.text LIKE '%demo-remote.png%')")]
    c.execute("INSERT OR REPLACE INTO settings VALUES('archived_conversation_ids',?)",(json.dumps(old_chats),))
    c.execute("UPDATE messages SET text='I cannot open Netflix. Could Emma help me with the remote?' WHERE speaker='caller' AND conversation_id IN (SELECT id FROM conversations WHERE demo=1)")
    # Only seeded examples get new wording. The user's actual phone call stays intact.
    c.execute("UPDATE records SET body=? WHERE id='rbc' AND source='seed'",('Emma Hayes is the fictional granddaughter and primary dashboard contact. Daniel Hayes is the backup. No real phone numbers are configured for these characters.',))
    c.execute("UPDATE conversations SET summary='Sample: June asked for help opening Netflix.' WHERE demo=1")
    c.execute("UPDATE occurrences SET evidence='Sample: June could not open Netflix and asked Emma for help. This is a scripted example, not evidence of a broken TV.' WHERE conversation_id IN (SELECT id FROM conversations WHERE demo=1)")
    c.execute("UPDATE issues SET title='June needs a hand with the TV' WHERE topic='tv'")
    c.execute("INSERT OR REPLACE INTO settings VALUES('family_profile',?)",(json.dumps(DEFAULT_PROFILE),))
    c.execute("INSERT INTO settings VALUES('english_demo_v2','true')")
    store.event(c,'English demo prepared','Earlier prototype assets were archived. Original phone transcripts were retained.','migration')


def migrate_callback(c):
    """Retire old fixtures and keep product records factual; preserve original messages."""
    if c.execute("SELECT 1 FROM settings WHERE key='callback_plain_v1'").fetchone(): return
    archived=json.loads((c.execute("SELECT value FROM settings WHERE key='archived_record_ids'").fetchone() or ['[]'])[0])
    for rid in ('channel','pickup','parcel'):
        row=c.execute('SELECT source FROM records WHERE id=?',(rid,)).fetchone()
        if row and row['source'] in ('seed','simulation') and rid not in archived: archived.append(rid)
    c.execute("INSERT OR REPLACE INTO settings VALUES('archived_record_ids',?)",(json.dumps(archived),))
    profile_row=c.execute("SELECT value FROM settings WHERE key='family_profile'").fetchone()
    p={**DEFAULT_PROFILE,**(json.loads(profile_row[0]) if profile_row else {})}
    for rid,body in (
      ('rbc',p['member_name']+' is the primary family contact. '+p['backup_name']+' is the backup. Requests appear in the family dashboard.'),
      ('quiet','Everyday requests go to the family dashboard, where Emma can pick them up and add a response.')
    ):
        c.execute("UPDATE records SET body=?,version=version+1,updated_at=? WHERE id=? AND source IN ('seed','onboarding')",(body,store.now(),rid))
    c.execute("UPDATE records SET body=?,version=version+1,updated_at=? WHERE title=? AND body LIKE 'Fictional demo household setup%'",(HOUSEHOLD_NOTE.strip(),store.now(),"June's Roku streaming setup and remote"))
    c.execute("UPDATE resources SET text=? WHERE title='source-notes.md' AND status='ready'",(SOURCE_NOTE,))
    photo_note='Black Roku remote with a purple directional pad and OK in the middle. Home is the house-shaped button at the top right. The white Netflix key has red lettering and sits below the playback controls, left of Disney+. Photo by Texas Lane, Wikimedia Commons, CC BY-SA 4.0. Original unchanged. Source: '+PHOTO_SOURCE+' License: https://creativecommons.org/licenses/by-sa/4.0/'
    c.execute("UPDATE resources SET text=? WHERE title='roku-tv-remote.jpg' AND status='ready'",(photo_note,))
    c.execute("INSERT INTO settings VALUES('callback_plain_v1','true')")
    store.event(c,'Household information organized','TV setup and family contacts are ready for calls.','setup')
