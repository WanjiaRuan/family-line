import json
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient
from family import store, intelligence, resources, worker
from family.web import app


@pytest.fixture(autouse=True)
def isolated(tmp_path,monkeypatch):
    monkeypatch.setattr(store,"DATA",tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY",raising=False)
    monkeypatch.setenv("GUAVA_API_KEY","unit-test-placeholder")
    store.init()
    # Transaction tests own their fixture; retired presentation seeds stay archived.
    with store.db() as c:
        c.execute("INSERT INTO records VALUES(?,?,?,?,?,0,1,?,?)", (
            "test_preference", "preference", "Preferred volume", "Preferred volume is 20.",
            "test", store.now(), store.now(),
        ))


@pytest.fixture
def client():
    return TestClient(app,headers={"X-Family-Client":"local-ui"})


def change(**kw):
    return {"record_id":"test_preference","kind":"preference","title":"Preferred volume","body":"Preferred volume is 25.",**kw}


def test_no_secret_returned_and_private_file(client):
    assert client.post('/api/settings',json={"api_key":"test-placeholder-credential","model":"gpt-4.1-mini"}).status_code==200
    state=client.get('/api/state').text
    assert 'test-placeholder-credential' not in state
    assert intelligence.public_config()['configured']
    assert (store.DATA/'.provider.json').stat().st_mode & 0o777 == 0o600


def test_csrf_and_host_rejected(client):
    assert client.post('/api/records',json=change(),headers={"Origin":"https://evil.example"}).status_code==403
    assert client.get('/api/state',headers={"Host":"evil.example"}).status_code==403
    assert TestClient(app).post('/api/settings',json={}).status_code==403


def test_atomic_updates_and_versions(client):
    assert client.post('/api/records',json=change(expected_version=1)).status_code==200
    assert client.post('/api/records',json=change(body="wrong",expected_version=1)).status_code==400
    assert next(x for x in store.all_records() if x['id']=='test_preference')['body']=='Preferred volume is 25.'
    before=len(store.all_records())
    with pytest.raises(ValueError):
        store.apply_changes([change(record_id=None),change(record_id='missing')],'test')
    assert len(store.all_records())==before


def test_operation_idempotence():
    before=len(store.all_records())
    a=store.apply_changes([change(record_id=None)],'test','same-request')
    b=store.apply_changes([change(record_id=None)],'test','same-request')
    assert a==b
    assert len(store.all_records())==before+1


def test_repeat_issue_counts_independent_calls():
    store.start_conversation('one')
    for _ in range(4): store.add_issue('one','tv','TV','same conversation updates')
    issue=next(i for i in store.snapshot()['issues'] if i['topic']=='tv')
    assert issue['occurrences']==3
    store.start_conversation('two')
    store.add_issue('two','tv','TV','second distinct conversation')
    assert next(i for i in store.snapshot()['issues'] if i['topic']=='tv')['occurrences']==4


def test_utterance_revision_not_duplicate():
    store.start_conversation('one')
    store.message('one','caller','six','utterance-1')
    store.message('one','caller','sixty eight','utterance-1')
    messages=store.conversation('one')['messages']
    assert len(messages)==1 and messages[0]['text']=='sixty eight'


def test_parcel_event_dedup_and_collection_cancels():
    store.parcel_status('parcel','ready_for_pickup')
    store.parcel_status('parcel','ready_for_pickup')
    assert len(store.snapshot()['jobs'])==1
    store.parcel_status('parcel','collected','caller-report')
    assert store.snapshot()['jobs'][0]['status']=='cancelled'


def test_worker_single_delivery_and_restart_state():
    store.add_job('test',{'message':'test'},store.now(),dedup='one')
    worker.tick(); worker.tick()
    job=store.snapshot()['jobs'][0]
    assert job['status']=='delivered' and job['attempts']==1
    store.init()
    assert store.snapshot()['jobs'][0]['status']=='delivered'


def test_future_job_not_sent_and_phone_failure_visible():
    future=(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()
    store.add_job('future',{},future)
    worker.tick()
    assert store.snapshot()['jobs'][0]['status']=='pending'
    store.add_job('phone',{},store.now(),'phone')
    worker.tick()
    assert store.snapshot()['jobs'][0]['status']=='failed'


def test_naive_reminder_time_rejected():
    with pytest.raises(ValueError): store.add_job('bad',{},'2026-10-18T10:00')


def test_upload_text_is_readable_and_image_without_key_not_claimed(client):
    r=client.post('/api/resources/upload',files={'file':('guide.txt',b'The spare remote is in the kitchen drawer.','text/plain')})
    assert r.status_code==200 and r.json()['status']=='ready'
    assert 'kitchen drawer' in client.get('/api/resources/'+r.json()['id']).json()['text']
    r=client.post('/api/resources/upload',files={'file':('remote.png',b'fake-image-test','image/png')})
    assert r.json()['status']=='needs_model'
    assert client.get('/api/resources/'+r.json()['id']).json()['text']==''


@pytest.mark.parametrize('url',['http://127.0.0.1:8778','http://localhost','file:///etc/passwd','http://169.254.169.254','http://example.com:22','http://user:pass@example.com'])
def test_url_local_and_credential_targets_blocked(url):
    with pytest.raises(ValueError): resources.public_target(url)


def test_chat_requires_key_and_no_fake_reply(client):
    before=len(store.all_records())
    r=client.post('/api/chat',json={'text':'update my volume'})
    assert r.status_code==400
    assert 'API key' in r.json()['detail']
    assert len(store.all_records())==before


def test_retrieval_can_find_later_document_passage():
    resources.ingest((('unrelated introduction\n'*900)+'\nThe turquoise switch disables vacation mode.').encode(),'manual.txt','text/plain')
    result=json.loads(store.context('Where is the turquoise vacation switch?'))
    assert any('turquoise switch' in r['text'] for r in result['resource_excerpts'])


def test_model_proposal_does_not_write_until_confirmed(client,monkeypatch):
    monkeypatch.setattr(intelligence,'intake',lambda cid,text:{'reply':'Ready for review','changes':[change()]})
    r=client.post('/api/chat',json={'text':'update volume to 25'}).json()
    assert '20' in next(x for x in store.all_records() if x['id']=='test_preference')['body']
    assert client.post('/api/proposals/'+r['proposal_id']+'/confirm').status_code==200
    assert client.post('/api/proposals/'+r['proposal_id']+'/confirm').status_code==200
    assert next(x for x in store.all_records() if x['id']=='test_preference')['version']==2


class FakeCall:
    def __init__(self,role='grandma',fields=None):
        self.id='unit-call';self.vars={'role':role,'operation_key':'unit-op'};self.fields=fields or {};self.instructions=[]
        self.vars['pending_change']={k:v for k,v in self.fields.items() if k!='confirmed'}
        store.start_conversation(self.id,role)
    def get_variable(self,key,default=None):return self.vars.get(key,default)
    def get_field(self,key):return self.fields.get(key)
    def send_instruction(self,text):self.instructions.append(text)
    def add_info(self,*args):pass


def test_phone_role_enforced_at_backend():
    from family.phone import save_complete
    rid=store.apply_changes([change(record_id=None,kind='device')],'test')[0]
    call=FakeCall(fields={**change(record_id=rid,kind='preference'), 'confirmed':'yes'})
    save_complete(call)
    assert any('DID NOT SAVE' in s for s in call.instructions)
    assert next(x for x in store.all_records() if x['id']==rid)['kind']=='device'


def test_phone_save_confirmed_and_visible():
    from family.phone import save_complete
    call=FakeCall(fields={**change(),'confirmed':'yes'})
    save_complete(call);save_complete(call)
    record=next(x for x in store.all_records() if x['id']=='test_preference')
    assert record['body']=='Preferred volume is 25.' and record['version']==2
    assert any('BACKEND SUCCESS' in s for s in call.instructions)


def test_onboarding_persists_and_does_not_configure_real_calls(client):
    from family.demo import DEFAULT_PROFILE
    profile={k:v for k,v in DEFAULT_PROFILE.items() if k not in {'language','onboarded'}}
    assert client.post('/api/profile',json=profile).status_code==400
    profile['sharing_acknowledged']=True
    assert client.post('/api/profile',json=profile).status_code==200
    store.init()
    state=client.get('/api/state').json()
    assert state['profile']['onboarded'] and state['profile']['member_name']=='Emma Hayes'
    assert state['test_phone']==''


def test_chat_attachment_is_draft_until_atomic_handover(client,monkeypatch):
    cid=client.post('/api/conversations').json()['id']
    r=client.post('/api/resources/upload',data={'conversation_id':cid},files={'file':('setup.md',b'Roku remote is in the woven basket.','text/markdown')}).json()
    rid=r['id']
    assert client.get('/api/resources/'+rid).json()['status']=='needs_review'
    assert 'woven basket' not in store.context()
    monkeypatch.setattr(intelligence,'intake',lambda *args:{'reply':'Please review the handover.','changes':[change(record_id=None,kind='device',title='Roku',body='Remote in the woven basket.')],'resource_notes':[{'resource_id':rid,'text':'Observed: remote kept in a woven basket.'}]})
    p=client.post('/api/chat',json={'conversation_id':cid,'text':'Save the handover.'}).json()
    assert 'woven basket' not in store.context()
    assert client.post('/api/proposals/'+p['proposal_id']+'/confirm').status_code==200
    assert client.post('/api/proposals/'+p['proposal_id']+'/confirm').status_code==200
    assert client.get('/api/resources/'+rid).json()['status']=='ready'
    assert 'woven basket' in store.context()
    assert len([r for r in store.all_records() if r['title']=='Roku'])==1
    restored=client.get('/api/conversations/'+cid).json()
    assert restored['attachments'][0]['id']==rid and restored['proposals'][0]['status']=='saved'


def test_changed_resource_blocks_entire_handover(client,monkeypatch):
    cid=client.post('/api/conversations').json()['id']
    rid=client.post('/api/resources/upload',data={'conversation_id':cid},files={'file':('guide.txt',b'Original source.','text/plain')}).json()['id']
    monkeypatch.setattr(intelligence,'intake',lambda *args:{'reply':'Review','changes':[change()],'resource_notes':[{'resource_id':rid,'text':'Reviewed source'}]})
    pid=client.post('/api/chat',json={'conversation_id':cid,'text':'save'}).json()['proposal_id']
    with store.db() as c:c.execute('UPDATE resources SET text=? WHERE id=?',('Changed elsewhere',rid))
    assert client.post('/api/proposals/'+pid+'/confirm').status_code==400
    assert next(r for r in store.all_records() if r['id']=='test_preference')['version']==1
    assert client.get('/api/resources/'+rid).json()['status']=='needs_review'


def test_cannot_approve_another_conversations_resource(client,monkeypatch):
    first=client.post('/api/conversations').json()['id'];second=client.post('/api/conversations').json()['id']
    rid=client.post('/api/resources/upload',data={'conversation_id':first},files={'file':('private-note.txt',b'Only in first chat.','text/plain')}).json()['id']
    monkeypatch.setattr(intelligence,'intake',lambda *args:{'reply':'Review','changes':[],'resource_notes':[{'resource_id':rid,'text':'Borrowed'}]})
    assert client.post('/api/chat',json={'conversation_id':second,'text':'save'}).status_code==400


def test_retired_tv_guidance_cannot_conflict_with_real_photo():
    assert 'Silver remote controls the TV' not in store.context()
    assert not any(r['title']=='demo-remote.png' for r in store.snapshot()['resources'])
    with pytest.raises(ValueError):store.apply_changes([change(record_id='tv')],'web')


def test_resolution_note_is_available_to_next_call(client):
    assert client.post('/api/issues/issue_tv',json={'status':'resolved','owner':'Emma'}).status_code==400
    assert client.post('/api/issues/issue_tv',json={'status':'resolved','owner':'Emma','note':'I moved the remote to the blue tray and showed June the Netflix key.'}).status_code==200
    assert 'blue tray' in store.context()
    assert client.get('/api/issues/issue_tv').json()['notes'][0]['author']=='Emma'


def test_successful_tv_call_does_not_create_followup(monkeypatch):
    from family import phone
    from types import SimpleNamespace
    call=FakeCall()
    store.message(call.id,'caller','Netflix opened. It is working now.')
    before=next(i for i in store.snapshot()['issues'] if i['id']=='issue_tv')['occurrences']
    monkeypatch.setattr(phone,'generate',lambda *args,**kwargs:json.dumps({'topic':'tv','outcome':'resolved','summary':'Caller confirmed Netflix opened.'}))
    phone.ended(call,SimpleNamespace(termination_reason='completed'))
    assert next(i for i in store.snapshot()['issues'] if i['id']=='issue_tv')['occurrences']==before
    assert next(c for c in store.snapshot()['conversations'] if c['id']==call.id)['outcome']=='resolved'


def test_explicit_help_evidence_not_replaced_by_goodbye(monkeypatch):
    from family import phone
    from types import SimpleNamespace
    call=FakeCall();call.vars['help_requested']=True
    store.add_issue(call.id,'tv','Help','Home button did not show a menu; June asked Emma to help.')
    store.message(call.id,'caller','Thanks, goodbye.')
    monkeypatch.setattr(phone,'generate',lambda *args,**kwargs:json.dumps({'topic':'tv','outcome':'unknown','summary':'June requested help after Home did not respond.'}))
    phone.ended(call,SimpleNamespace(termination_reason='completed'))
    with store.db() as c:
        assert 'Home button' in c.execute('SELECT evidence FROM occurrences WHERE conversation_id=?',(call.id,)).fetchone()[0]
    assert next(c for c in store.snapshot()['conversations'] if c['id']==call.id)['outcome']=='needs_family'


def test_url_is_part_of_conversation_and_waits_for_confirmation(client,monkeypatch):
    cid=client.post('/api/conversations').json()['id']
    monkeypatch.setattr(resources,'fetch',lambda url:(b'<main>The purple arrows navigate Roku. The device model is unknown.</main>','text/html',url))
    r=client.post('/api/resources/url',json={'url':'https://example.com/remote','conversation_id':cid})
    assert r.status_code==200
    resource=client.get('/api/resources/'+r.json()['id']).json()
    assert resource['status']=='needs_review' and resource['url']=='https://example.com/remote'
    assert 'purple arrows' not in store.context()
    assert client.get('/api/conversations/'+cid).json()['attachments'][0]['id']==resource['id']


def test_retry_does_not_publish_conversation_draft(client):
    cid=client.post('/api/conversations').json()['id']
    rid=client.post('/api/resources/upload',data={'conversation_id':cid},files={'file':('note.txt',b'New home fact.','text/plain')}).json()['id']
    assert client.post('/api/resources/'+rid+'/retry').json()['status']=='needs_review'
    assert 'New home fact.' not in store.context()


def test_new_photo_draft_does_not_hide_previously_approved_photo():
    from family.demo import setup_status
    with store.db() as c:
        c.execute('INSERT INTO resources VALUES(?,?,?,?,?,?,?,?,?)',('approved-photo','roku-tv-remote.jpg','image/jpeg',None,None,'Reviewed photo notes','ready',None,'2026-10-17T10:00:00+00:00'))
        c.execute('INSERT INTO resources VALUES(?,?,?,?,?,?,?,?,?)',('new-photo','roku-tv-remote.jpg','image/jpeg',None,None,'New draft','needs_review',None,'2026-10-17T11:00:00+00:00'))
    assert setup_status()['photo']['id']=='approved-photo'


def test_retired_channel_preference_stays_archived(client):
    assert not any(r["id"] == "channel" for r in store.all_records())
    context = json.loads(store.context("What would June like to watch?"))
    assert not any(r["id"] == "channel" for r in context["records"])
    response = client.post("/api/records", json=change(record_id="channel"))
    assert response.status_code == 400 and "archived" in response.json()["detail"]
