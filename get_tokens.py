import json
import twitter

def get_tokens():
    creds['access_token'], creds['access_token_secret'] = twitter.oauth_dance("",creds['consumer_key'],creds['consumer_secret'])
    with open("credentials-new.json",'wb') as fh:
        json.dump(creds,fh,indent=1)

with open("credentials.json") as fh:
    creds = json.load(fh)

if 'access_token' in creds:
    print "looks like you've already got a token"
else:
    get_tokens()