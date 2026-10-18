"""Family Line: local dashboard and Guava telephone share one SQLite database.

Run: guava run /Users/rbc/demo-agent -- --phone
Dashboard only: uv run python main.py
Original tutorial: uv run python main.todo.py
"""
import argparse
import logging
import threading
import tomllib
import uvicorn
from family import store, worker


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phone',action='store_true',help='Also listen on the Guava project phone number')
    parser.add_argument('--chat',action='store_true',help='Guava text conversation instead of web server')
    parser.add_argument('--voice',action='store_true',help='Guava local microphone instead of web server')
    parser.add_argument('--port',type=int,default=8778)
    parser.add_argument('--verify-live',action='store_true',help='Run bounded Guava text integration checks')
    parser.add_argument('--verify-case',choices=['preference','family','support','delivery','television'],default='preference')
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpx2').setLevel(logging.WARNING)
    store.init()
    if args.verify_live:
        if args.verify_case=="television":
            from family.tv_check import run
            run()
        else:
            from family.live_check import run
            run(args.verify_case)
        return
    if args.chat or args.voice:
        from family.phone import agent
        if args.chat: agent.chat()
        else: agent.call_local()
        return
    from family.web import app
    stop=threading.Event()
    dial=None
    if args.phone:
        from family.phone import agent
        with (store.ROOT/'guava.toml').open('rb') as f:
            number=tomllib.load(f)['phone_number']
        store.put_setting('phone_status',{'state':'starting','number':number})
        class ListenerStatus(logging.Handler):
            def emit(self,record):
                if 'Started listing on phone number' in record.getMessage():
                    store.put_setting('phone_status',{'state':'listening','number':number})
        logging.getLogger('guava.agent').addHandler(ListenerStatus())
        def listen():
            while not stop.is_set():
                try:
                    agent.listen_phone(number)
                except Exception:
                    logging.getLogger('family').error('Guava listener disconnected; retrying.')
                store.put_setting('phone_status',{'state':'offline','number':number})
                stop.wait(5)
        threading.Thread(target=listen,daemon=True).start()
        dial=lambda destination,message: agent.call_phone(number,destination,{'outbound_message':message})
    else:
        store.put_setting('phone_status',{'state':'offline'})
    threading.Thread(target=worker.run,args=(stop,dial),daemon=True).start()
    try:
        uvicorn.run(app,host='127.0.0.1',port=args.port,access_log=False)
    finally:
        stop.set()
        store.put_setting('phone_status',{'state':'offline'})


if __name__=='__main__':
    main()
