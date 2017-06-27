from subprocess import call
import threading
import time
from creds import *



def run_bot(puppet, posting_key):
    call(["python3", "multibot.py", puppet, posting_key])


for ea_acct in accounts:
    try:
        pupp_pk = accounts[ea_acct]['posting_key']
        t = threading.Thread(target=run_bot, args=(ea_acct, pupp_pk))
        t.start()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting...")
        t.close()
        sys.exit(0)
