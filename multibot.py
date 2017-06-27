import random
from piston.steem import *
from piston.exceptions import InvalidWifError, PostDoesNotExist
from pistonapi.exceptions import VoteWeightTooSmall
import threading
import traceback
import time
import sys

upvote_history = []
MAX_THREADS = 4
running_threads = []
lock = threading.Lock()
users_to_follow = ['minnowpond']



def curation_delay_vote(wif_key, account_to_vote_with, identifier, time_to_wait):
    print(time_to_wait)
    time.sleep(time_to_wait)
    steem = Steem(wif=wif_key)
    steem.vote(identifier, 100, account_to_vote_with)
    print("[INFO][FOLLOW][VOTE] Voted")


def multifollower(puppet, puppet_posting_key):
    print("{} : Waiting for new upvotes from {}".format(puppet, users_to_follow))
    steem = Steem(wif=puppet_posting_key)
    pupp = Account(puppet)
    if pupp.voting_power() >= 70:
        for user in users_to_follow:
            for comment in steem.get_account_history(user):
                operation = comment[1]['op']
                timestamp = comment[1]['timestamp']
                if timestamp > '2017-06-20T01:00:00' and operation[0] == 'vote':
                    print("VOTEOP:{}".format(operation[1]))
                    voter = operation[1]['voter']
                    author = operation[1]['author']
                    permalink = operation[1]['permlink']
                    post = steem.get_post("{}/{}".format(author, permalink))
                    identifier = "{}/{}".format(author, permalink)
                    if voter in users_to_follow:
                        print("New upvote by @{} {}".format(voter, url_builder(post)))
                        if identifier in upvote_history:
                            continue
                        try:
                            print("Voting from {} account".format(puppet))
                            curation_time = random.randint(1800, 2200)
                            dice = random.randint(1, 100)
                            if dice > 60:
                                print("POST Dice:{}".format(dice))
                                t = threading.Thread(target=curation_delay_vote,
                                                     args=(puppet_posting_key, puppet, identifier, curation_time))
                                t.start()
                                upvote_history.append(identifier)
                            else:
                                print("Failed dice:{}".format(dice))
                        except Exception as e:
                            print("Upvoting failed...")
                            print("We have probably reached the upvote rate limit.")
                            print("ERROR: {}".format(str(e)))
    else:
        print("Skipping vote from {} due to low voting power: {}".format(puppet, pupp.voting_power()))
        pass





def url_builder(comment):
    return "https://steemit.com/%s/%s" % (comment.category, comment.identifier)


if __name__ == "__main__":
    while True:
        try:
           puppet = sys.argv[1]
           posting_key = sys.argv[2]
           multifollower(puppet, posting_key)
        except (KeyboardInterrupt, SystemExit):
            print("Quitting...")
            break
        except Exception as err:
            print('### Exception Occurred: Restarting:   {}'.format(err))
            print("{}:   Unexpected error: {}".format(puppet, sys.exc_info()[0]))
            traceback.print_exc()
