"""Live Guava checks; use FAMILY_DATA_DIR to isolate the test database."""
import json
import signal
from . import store
from .phone import agent


def run(case="preference"):
    def expired(*_):
        raise TimeoutError("Guava live test exceeded 200 seconds.")
    signal.signal(signal.SIGALRM,expired)
    signal.alarm(200)
    try:
        if case=='delivery':
            store.parcel_status('parcel','ready_for_pickup')
        with agent.test(variables={"test_mode":True}) as session:
            session.wait_for_turn()
            print("GREETING",session.get_transcript(),flush=True)
            turns={"preference":[
                "I'm trying the grandmother role.",
                "Please update my saved favorite TV channel to channel 68 instead of 67.",
                "Yes, please save that change.",
            ],"family":[
                "I'm the family information provider.",
                "Please add a new household note: the spare silver remote is in the kitchen drawer.",
                "Yes, please save that note.",
            ],"support":[
                "I'm trying the grandmother role.",
                "My TV says no signal. I have the silver remote.",
                "I selected HDMI one and pressed OK, but there is still no picture. Please leave a request for my family to help me with the television.",
                "The TV still has no signal after selecting HDMI one. Please save that request for my family in the dashboard.",
            ],"delivery":[
                "I'm trying the grandmother role.",
                "Has my rice cooker parcel arrived? Where should I pick it up?",
                "I've already picked up the rice cooker parcel. Please mark it collected.",
            ]}[case]
            for text in turns:
                session.say(text)
                session.wait_for_turn()
                print("TURN",session.get_transcript().splitlines()[-4:],flush=True)
            record=next(r for r in store.all_records() if r['id']=='channel')
            print("SAVED_RECORD",json.dumps({k:record[k] for k in ('id','body','version','source')}),flush=True)
            session.say({"preference":"What is my favorite channel now?","family":"Where is the spare silver remote?","support":"Has someone in my family already been called?","delivery":"Is there still a pickup reminder pending for my rice cooker?"}[case])
            session.wait_for_turn()
            print("QUERY",session.get_transcript().splitlines()[-4:],flush=True)
            session.say("Thank you, goodbye. Please hang up now.")
            session.wait_for_end()
            print("TRANSCRIPT\n"+session.get_transcript(),flush=True)
            if case=="preference":
                assert '68' in record['body'] and record['version']>1, "Preference was not persisted"
            if case=="family":
                assert any('kitchen drawer' in r['body'].lower() and r['source'].startswith('phone:') for r in store.all_records()), "Family note was not persisted"
            if case=="support":
                with store.db() as c:
                    assert c.execute("SELECT 1 FROM events WHERE title='Family follow-up created' AND source='phone'").fetchone(), "Family request callback did not complete"
            if case=='delivery':
                parcel=next(r for r in store.all_records() if r['id']=='parcel')
                assert json.loads(parcel['body'])['status']=='collected', 'Parcel collection was not recorded'
                assert store.snapshot()['jobs'][0]['status']=='cancelled', 'Pending pickup reminder not cancelled'
            assert len(store.conversation(session.id)['messages'])>=4, "Live speech did not reach database"
        print("LIVE_GUAVA_"+case.upper()+"_PASS",flush=True)
    finally:
        signal.alarm(0)
