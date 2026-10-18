"""Guava model test with fictional TV material only; no PSTN calls or prior transcripts."""
import json
import signal
import time
from . import store
from .phone import agent


def wait_for_outcome(cid):
    deadline=time.monotonic()+50
    while time.monotonic()<deadline:
        with store.db() as c:
            row=c.execute('SELECT outcome FROM call_outcomes WHERE conversation_id=?',(cid,)).fetchone()
        if row:return row[0]
        time.sleep(.25)
    raise AssertionError('End-of-call summary did not finish within 50 seconds.')


def run():
    def timeout(*_): raise TimeoutError('TV model check exceeded 240 seconds.')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(240)
    try:
        assert any('woven basket' in r['body'].lower() for r in store.all_records()), 'A fictional reviewed TV setup is required.'
        with store.db() as c: before=c.execute('SELECT COUNT(*) FROM occurrences').fetchone()[0]
        with agent.test(variables={'test_mode':True}) as session:
            session.wait_for_turn()
            for message in ["I'm June, the grandmother.","I'd like to watch Netflix but I don't know which remote to use. Where is my Roku remote?","I found the black remote with purple arrows. Which button should I press to open Netflix?","I pressed the white Netflix button. Netflix opened and that solved my problem. Thank you.","Goodbye. Please hang up now."]:
                session.say(message)
                if 'hang up' in message:session.wait_for_end()
                else:session.wait_for_turn()
            transcript=session.get_transcript()
            print('SUCCESS CALL\n'+transcript,flush=True)
            assert 'basket' in transcript.lower(),'Saved location was not used.'
            assert wait_for_outcome(session.id)=='resolved','Successful call outcome was not retained.'
            with store.db() as c:
                assert c.execute('SELECT COUNT(*) FROM occurrences').fetchone()[0]==before,'Successful guidance created a follow-up.'
        with agent.test(variables={'test_mode':True}) as session:
            session.wait_for_turn()
            for message in ["I'm June, the grandmother.","My TV screen is black. I pressed Home on the black Roku remote but the menu did not appear. Is its red button the input button?","I cannot find a labeled input button. Please leave a request for Emma to help me.","Please save that request: the TV stayed black after pressing Home on the Roku remote. I need Emma's help.","Has Emma already been called?","Thank you. Goodbye. Please hang up now."]:
                session.say(message)
                if 'hang up' in message:session.wait_for_end()
                else:session.wait_for_turn()
            print('FOLLOW-UP CALL\n'+session.get_transcript(),flush=True)
            assert wait_for_outcome(session.id)=='needs_family','Explicit help request was lost.'
            with store.db() as c:
                occurrence=c.execute('SELECT evidence FROM occurrences WHERE conversation_id=?',(session.id,)).fetchone()
                assert occurrence and ('home' in occurrence[0].lower() or 'black' in occurrence[0].lower()),'Relevant help evidence was not saved.'
        print('TV_DEMO_LIVE_PASS',flush=True)
    finally:signal.alarm(0)
