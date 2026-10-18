import json
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import store, intelligence, resources, demo

app=FastAPI(title="Family Line",docs_url=None,redoc_url=None,openapi_url=None)
STATIC=Path(__file__).parent / "static"


@app.middleware("http")
async def local_only(request: Request,call_next):
    host=request.headers.get("host","").split(":")[0]
    if host not in {"127.0.0.1","localhost","testserver"}:
        return JSONResponse({"detail":"Only local access is allowed."},status_code=403)
    origin=request.headers.get("origin")
    if origin and origin!=str(request.base_url).rstrip("/"):
        return JSONResponse({"detail":"Cross-site requests are not allowed."},status_code=403)
    if request.method not in {"GET","HEAD"} and request.headers.get("x-family-client")!="local-ui":
        return JSONResponse({"detail":"Missing local client header."},status_code=403)
    try:
        if int(request.headers.get("content-length","0"))>resources.MAX_BYTES+50000:
            return JSONResponse({"detail":"Request exceeds the size limit."},status_code=413)
    except ValueError:
        return JSONResponse({"detail":"Invalid request length."},status_code=400)
    response=await call_next(request)
    response.headers["Cache-Control"]="no-store"
    response.headers["X-Content-Type-Options"]="nosniff"
    response.headers["Referrer-Policy"]="no-referrer"
    response.headers["Content-Security-Policy"]="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'"
    return response


@app.exception_handler(ValueError)
async def bad_input(request,exc):
    return JSONResponse({"detail":str(exc)},status_code=400)


@app.get("/")
def home():
    return FileResponse(STATIC / "index.html")


@app.get("/api/state")
def state():
    return {**store.snapshot(),"provider":intelligence.public_config(),"test_phone":store.setting("test_phone",""),"profile":demo.profile(),"demo_setup":demo.setup_status()}


class Settings(BaseModel):
    api_key: str=Field(default="",max_length=512)
    model: str="gpt-4.1-mini"
    test_phone: str=""


@app.post("/api/settings")
def settings(body: Settings):
    if body.test_phone and not re.fullmatch(r"\+[1-9]\d{7,14}",body.test_phone):
        raise ValueError("Use an international phone number, for example +1…; or leave it blank.")
    intelligence.save_config(body.api_key.strip(),body.model.strip())
    store.put_setting("test_phone",body.test_phone)
    return {"ok":True,**intelligence.public_config()}


@app.post("/api/settings/test")
def test_settings():
    return intelligence.test_connection()


class RecordInput(BaseModel):
    record_id: str | None=None
    kind: str
    title: str
    body: str
    expected_version: int | None=None


@app.post("/api/records")
def record(body:RecordInput):
    return {"ids":store.apply_changes([body.model_dump()],"web")}


@app.delete("/api/records/{rid}")
def delete_record(rid:str):
    with store.db() as c:
        record=c.execute("SELECT * FROM records WHERE id=?",(rid,)).fetchone()
        if not record:
            raise ValueError("Record not found.")
        if record["kind"]=="delivery":
            raise ValueError("Update demo parcels using parcel actions.")
        c.execute("DELETE FROM records WHERE id=?",(rid,))
        store.event(c,"Information removed",record["title"],"web",rid)
    return {"ok":True}


@app.get("/api/conversations/{cid}")
def conversation(cid:str):
    conv=store.conversation(cid)
    with store.db() as c:
        conv['attachments']=[dict(r) for r in c.execute("SELECT r.id,r.title,r.mime,r.status,r.created_at FROM resources r JOIN conversation_resources cr ON cr.resource_id=r.id WHERE cr.conversation_id=? AND r.status!='archived'",(cid,))]
        conv['proposals']=[{**dict(r),'changes':json.loads(r['changes']),'resource_notes':[dict(n) for n in c.execute('SELECT resource_id,text FROM proposal_resources WHERE proposal_id=?',(r['id'],))]} for r in c.execute('SELECT * FROM proposals WHERE conversation_id=? ORDER BY created_at',(cid,))]
    return conv


@app.get("/api/issues/{iid}")
def issue(iid:str):
    with store.db() as c:
        r=c.execute("SELECT * FROM issues WHERE id=?",(iid,)).fetchone()
        if not r:
            raise ValueError("Follow-up not found.")
        occurrences=[dict(x) for x in c.execute("SELECT o.*,c.channel,c.demo FROM occurrences o JOIN conversations c ON c.id=o.conversation_id WHERE issue_id=? ORDER BY o.created_at DESC",(iid,))]
        notes=[dict(n) for n in c.execute('SELECT * FROM issue_notes WHERE issue_id=? ORDER BY created_at DESC',(iid,))]
    return {**dict(r),"occurrences":occurrences,"notes":notes}


class IssueInput(BaseModel):
    status:str
    owner:str=""
    note:str=Field(default="",max_length=4000)


@app.post("/api/issues/{iid}")
def update_issue(iid:str,body:IssueInput):
    if body.status=='resolved' and not body.note.strip():
        raise ValueError('Add a brief resolution note so the next call has useful context.')
    store.set_issue(iid,body.status,body.owner)
    if body.note.strip():
        with store.db() as c:
            c.execute('INSERT INTO issue_notes VALUES(?,?,?,?,?)',(store.ident('note'),iid,body.owner or demo.profile()['member_name'],body.note.strip(),store.now()))
    return {"ok":True}


class ChatInput(BaseModel):
    text:str=Field(min_length=1,max_length=12000)
    conversation_id:str | None=None


@app.post("/api/chat")
def chat(body:ChatInput):
    cid=body.conversation_id or store.ident("chat")
    if body.conversation_id:
        existing=store.conversation(cid)
        if existing["channel"]!="web":
            raise ValueError("Web messages cannot be added to a phone call.")
    else:
        store.start_conversation(cid,"family","web")
    with store.db() as c:
        c.execute("UPDATE conversations SET state='active',ended_at=NULL WHERE id=?",(cid,))
    store.message(cid,"caller",body.text)
    versions={r["id"]:r["version"] for r in store.all_records()}
    try:
        result=intelligence.intake(cid,body.text)
    except intelligence.ProviderError as exc:
        store.message(cid,"system",str(exc))
        raise
    store.message(cid,"agent",result["reply"])
    pid=None
    notes=result.get("resource_notes",[])
    if result["changes"] or notes:
        for change in result["changes"]:
            if change.get("record_id"):
                change["expected_version"]=versions.get(change["record_id"])
        with store.db() as c:
            available={r['id']:dict(r) for r in c.execute("SELECT r.* FROM resources r JOIN conversation_resources cr ON cr.resource_id=r.id WHERE cr.conversation_id=?",(cid,))}
        for note in notes:
            if note['resource_id'] not in available or available[note['resource_id']]['status'] not in {'ready','needs_review'}:
                raise ValueError('The proposed attachment is unavailable. Please retry the conversation.')
        pid=store.ident("proposal")
        with store.db() as c:
            c.execute("INSERT INTO proposals VALUES(?,?,?,?,?)",(pid,cid,json.dumps(result["changes"],ensure_ascii=False),"pending",store.now()))
            for note in notes:
                c.execute('INSERT INTO proposal_resources VALUES(?,?,?,?)',(pid,note['resource_id'],note['text'],available[note['resource_id']]['text']))
    return {"conversation_id":cid,"reply":result["reply"],"changes":result["changes"],"resource_notes":notes,"proposal_id":pid}


@app.post("/api/proposals/{pid}/confirm")
def confirm(pid:str):
    with store.db() as c:
        c.execute('BEGIN IMMEDIATE')
        p=c.execute('SELECT * FROM proposals WHERE id=?',(pid,)).fetchone()
        if not p: raise ValueError('Proposal not found.')
        if p['status']=='saved': return {'ok':True,'already_saved':True}
        notes=c.execute('SELECT * FROM proposal_resources WHERE proposal_id=?',(pid,)).fetchall()
        for note in notes:
            current=c.execute('SELECT text,status FROM resources WHERE id=?',(note['resource_id'],)).fetchone()
            if not current or current['text']!=note['expected_text'] or current['status'] not in {'ready','needs_review'}:
                raise ValueError('An attachment changed. Ask the assistant to prepare a fresh handover.')
        changes=json.loads(p['changes'])
        ids=store.apply_changes_in(c,changes,'web-chat',op_key=pid) if changes else []
        for note in notes:
            c.execute("UPDATE resources SET text=?,status='ready',error=NULL WHERE id=?",(note['text'],note['resource_id']))
        c.execute("UPDATE proposals SET status='saved' WHERE id=?",(pid,))
        c.execute("UPDATE conversations SET state='ended',ended_at=? WHERE id=?",(store.now(),p['conversation_id']))
        store.event(c,'Handover saved',f'{len(ids)} family records and {len(notes)} resources are ready for calls.','web-chat',p['conversation_id'])
    return {'ids':ids,'resources':len(notes)}


def attach_to_conversation(cid,rid):
    conv=store.conversation(cid)
    if conv['channel']!='web': raise ValueError('Attachments require a family web conversation.')
    with store.db() as c:
        c.execute('INSERT OR IGNORE INTO conversation_resources VALUES(?,?)',(cid,rid))
        c.execute("UPDATE resources SET status='needs_review',error=NULL WHERE id=? AND status='ready'",(rid,))


@app.post('/api/conversations')
def new_conversation():
    cid=store.ident('chat')
    store.start_conversation(cid,'family','web')
    return {'id':cid}


class FamilyProfile(BaseModel):
    household_name:str=Field(max_length=100)
    member_name:str=Field(max_length=100)
    relationship:str=Field(max_length=100)
    elder_name:str=Field(max_length=100)
    elder_call_name:str=Field(max_length=100)
    backup_name:str=Field(max_length=100)
    backup_relationship:str=Field(default='Son',max_length=100)
    timezone:str=Field(max_length=80)
    sharing_acknowledged:bool


@app.post('/api/profile')
def save_profile(body:FamilyProfile):
    return demo.save_profile(body.model_dump())


@app.get('/api/demo/kit')
def demo_kit():
    import io,zipfile
    from fastapi.responses import Response
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
        for name in ('roku-tv-remote.jpg','household-note.txt','source-notes.md'):
            z.write(demo.ASSETS/name,name)
    return Response(buf.getvalue(),media_type='application/zip',headers={'Content-Disposition':'attachment; filename="family-line-tv-materials.zip"'})


@app.post("/api/resources/upload")
async def upload(file:UploadFile=File(...),conversation_id:str|None=Form(None)):
    if conversation_id and store.conversation(conversation_id)['channel']!='web':
        raise ValueError('Attachments require a family web conversation.')
    name=Path(file.filename or "upload").name
    if Path(name).suffix.lower() not in resources.EXTS:
        raise ValueError("Supported files: PDF, TXT, MD, DOCX, PNG, JPG and WebP.")
    data=await file.read(resources.MAX_BYTES+1)
    # Parsing/network calls run off the ASGI event loop.
    from starlette.concurrency import run_in_threadpool
    r=await run_in_threadpool(resources.ingest,data,name,file.content_type or "application/octet-stream")
    if conversation_id:
        attach_to_conversation(conversation_id,r['id'])
        r['conversation_id']=conversation_id
    return r


class URLInput(BaseModel):
    url:str=Field(max_length=2048)
    conversation_id:str|None=None


@app.post("/api/resources/url")
def import_url(body:URLInput):
    if body.conversation_id and store.conversation(body.conversation_id)['channel']!='web':
        raise ValueError('Links require a family web conversation.')
    try:
        data,mime,url=resources.fetch(body.url.strip())
    except (OSError,TimeoutError):
        raise ValueError("Could not fetch the link. No summary was generated.") from None
    name=unquote(urlsplit(url).path.rsplit("/",1)[-1]) or urlsplit(url).hostname
    r=resources.ingest(data,name,mime,url)
    if body.conversation_id: attach_to_conversation(body.conversation_id,r['id'])
    return r


@app.get("/api/resources/{rid}")
def get_resource(rid:str):
    with store.db() as c:
        r=c.execute("SELECT * FROM resources WHERE id=?",(rid,)).fetchone()
    if not r:
        raise ValueError("Resource not found.")
    data=dict(r)
    data["has_file"]=bool(data.pop("path"))
    return data


@app.get("/api/resources/{rid}/original")
def download_resource(rid:str):
    with store.db() as c:
        r=c.execute("SELECT * FROM resources WHERE id=?",(rid,)).fetchone()
    if not r or not r["path"]:
        raise ValueError("No original file is available.")
    return FileResponse(r["path"],filename=r["title"],media_type="application/octet-stream")


@app.get('/api/resources/{rid}/preview')
def preview_resource(rid:str):
    with store.db() as c:
        r=c.execute('SELECT path,mime FROM resources WHERE id=?',(rid,)).fetchone()
    if not r or not r['path'] or r['mime'] not in {'image/png','image/jpeg','image/webp'}:
        raise ValueError('No image preview is available.')
    return FileResponse(r['path'],media_type=r['mime'])


@app.post("/api/resources/{rid}/retry")
def retry_resource(rid:str):
    result=resources.retry(rid)
    with store.db() as c:
        if c.execute('SELECT 1 FROM conversation_resources WHERE resource_id=?',(rid,)).fetchone():
            c.execute("UPDATE resources SET status='needs_review' WHERE id=? AND status='ready'",(rid,))
            if result['status']=='ready': result['status']='needs_review'
    return result


class ResourceEdit(BaseModel):
    text:str=Field(min_length=1,max_length=150000)


@app.post("/api/resources/{rid}/confirm")
def confirm_resource(rid:str,body:ResourceEdit):
    with store.db() as c:
        if not c.execute("UPDATE resources SET text=?,status='ready',error=NULL WHERE id=?",(body.text,rid)).rowcount:
            raise ValueError("Resource not found.")
        store.event(c,"Resource reviewed",rid,"web",rid)
    return {"ok":True}


@app.delete("/api/resources/{rid}")
def delete_resource(rid:str):
    with store.db() as c:
        r=c.execute("SELECT path FROM resources WHERE id=?",(rid,)).fetchone()
        if not r:
            raise ValueError("Resource not found.")
        c.execute("DELETE FROM resources WHERE id=?",(rid,))
        store.event(c,"Resource removed",rid,"web",rid)
    if r["path"]:
        Path(r["path"]).unlink(missing_ok=True)
    return {"ok":True}


@app.post("/api/audio")
async def audio(file:UploadFile=File(...)):
    data=await file.read(resources.MAX_BYTES+1)
    if len(data)>resources.MAX_BYTES:
        raise ValueError("Recording exceeds 10 MB.")
    from starlette.concurrency import run_in_threadpool
    text=await run_in_threadpool(intelligence.transcribe,data)
    return {"text":text}


class JobInput(BaseModel):
    title:str=Field(min_length=1,max_length=500)
    due_at:str
    mode:str="dashboard"


@app.post("/api/jobs")
def create_job(body:JobInput):
    if body.mode=="phone" and not store.setting("test_phone"):
        raise ValueError("Set your own test recipient number first.")
    return {"id":store.add_job(body.title,{"message":body.title},body.due_at,body.mode)}


@app.post("/api/jobs/{jid}/cancel")
def cancel_job(jid:str):
    with store.db() as c:
        if not c.execute("UPDATE jobs SET status='cancelled',result='Cancelled by user' WHERE id=? AND status='pending'",(jid,)).rowcount:
            raise ValueError("Only pending reminders can be cancelled.")
    return {"ok":True}


class ParcelInput(BaseModel):
    status:str


@app.post("/api/parcels/{rid}/simulate")
def simulate_parcel(rid:str,body:ParcelInput):
    store.parcel_status(rid,body.status)
    return {"ok":True,"mode":"simulation"}


@app.post("/api/demo/tv-call")
def demo_tv_call():
    cid=store.ident("demo")
    store.start_conversation(cid,"grandma","simulation",True)
    store.message(cid,"caller","The TV says no signal again. Can you ask my family to help?")
    store.message(cid,"agent","[Scripted demo] I have added a request to the family dashboard; no one has been called.")
    store.add_issue(cid,"tv","Help with the living-room TV","Scripted sample: Roku Home did not appear; June asked Emma to help.")
    store.end_conversation(cid,"Scripted sample: TV assistance is still needed.")
    with store.db() as c:
        store.event(c,"Sample TV call added","Scripted sample only; no model call or phone call was made.","simulation",cid)
    return {"conversation_id":cid}


app.mount("/static",StaticFiles(directory=STATIC),name="static")
