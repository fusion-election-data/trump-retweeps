# -*- coding: UTF-8 -*-
import json
import time
import traceback
import twitter

with open("credentials.json") as fh:
    creds = json.load(fh)

auth=twitter.OAuth(creds['access_token'],
                   creds['access_token_secret'],
                   creds['consumer_key'],
                   creds['consumer_secret'])

t = twitter.Twitter(auth=auth)
ts = twitter.TwitterStream(auth=auth)


def get_user_bio(user):
    try:
        urls = user['entities']['description']['urls']
    except:
        print "******* User Entities Fail"
        print user
        urls = []
    text = user['description']
    # TODO: Handle the case where a URL crosses the truncation point
    if len(text) > 140:
        text = text[:139] + u"…"
    for url in urls:
        text = text.replace(url['url'],url['expanded_url'])
    return text

def get_tweet_bio(tweet):
    if 'retweeted_status' in tweet:
        uid = tweet['retweeted_status']['user']['id']
        return get_user_bio(t.users.show(user_id=uid))
    elif tweet['text'].startswith('"'):
        for um in tweet['entities']['user_mentions']:
            if um['indices'][0] == 1:
                return get_user_bio(t.users.show(user_id=um['id']))

def do_tweet(tweet):
    try:
        if 'text' in tweet and tweet['user']['id']==creds['target_uid']:
            bio = get_tweet_bio(tweet)
            if bio:
                t.statuses.update(status=bio)
    except twitter.api.TwitterHTTPError:
        print "twitter api error"
        traceback.print_exc()


def catchAndPrintExceptions(func):
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print "caught!"
            traceback.print_exc()
            time.sleep(5)
    return wrapped

@catchAndPrintExceptions
def followStream():
    follow_stream = ts.statuses.filter(follow=creds['target_uid'])
    for tweet in follow_stream:
        do_tweet(tweet)

# for tweet in reversed(t.statuses.user_timeline(user_id=creds['target_uid'],count=200)):
#     do_tweet(tweet)

while True:
    followStream()