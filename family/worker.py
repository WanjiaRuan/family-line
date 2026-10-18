import json
import threading
import logging
from . import store


def tick(dial=None):
    with store.db() as c:
        # Atomically claim one due job. In-flight calls never auto-retry after restart.
        c.execute("BEGIN IMMEDIATE")
        job=c.execute("SELECT * FROM jobs WHERE status='pending' AND due_at<=? ORDER BY due_at LIMIT 1",(store.now(),)).fetchone()
        if not job:
            return
        c.execute("UPDATE jobs SET status='running',attempts=attempts+1 WHERE id=?",(job["id"],))
    payload=json.loads(job["payload"])
    status,result="delivered","Shown in the dashboard; this does not mean a family member has read it."
    try:
        if job["mode"]=="phone":
            destination=store.setting("test_phone","")
            if not dial or not destination:
                raise ValueError("Phone connection or test recipient is not configured.")
            dial(destination,payload.get("message",job["title"]))
            status,result="attempted","Dialing finished. Check the call record; task completion is not confirmed."
        with store.db() as c:
            store.event(c,"Reminder is due",job["title"],job["mode"],job["id"])
    except Exception:
        status,result="failed","Reminder failed. Check connection settings before rescheduling. No automatic redial."
    with store.db() as c:
        c.execute("UPDATE jobs SET status=?,result=? WHERE id=?",(status,result,job["id"]))


def run(stop: threading.Event,dial=None):
    with store.db() as c:
        c.execute("UPDATE jobs SET status='interrupted',result='Execution was interrupted. Check whether contact was made before rescheduling.' WHERE status='running'")
    while not stop.is_set():
        try:
            tick(dial)
        except Exception:
            logging.getLogger("family.worker").exception("Scheduled task cycle failed; next cycle will retry availability.")
        stop.wait(2)
