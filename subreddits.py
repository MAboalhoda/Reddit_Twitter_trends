import requests, os

##############OAuth authentication###############

CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
SECRET_KEY = os.environ.get('REDDIT_SECRET_KEY')

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': "password",
    'username': os.environ.get('REDDIT_USERNAME'),
    'password': os.environ.get('REDDIT_PW')
}

headers = {"User-Agent": 'API/business/0.01'}

res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
HEADERS= {**headers, **{'Authorization': f"bearer {TOKEN}"}}

######################requesting subreddit names from the reddit API##########

class Subreddit_Names():
    def __init__(self):
        pass

    def sr_names(self):
        end_point = 'https://oauth.reddit.com'
        sr_names = '/api/search_reddit_names'
        suggested_topic = ['wallstreet','cryptocurrency','business','stocks']
        self.sr_list = []
        for topic in suggested_topic:
            params ={
                'query' : topic
            }

            res = requests.get(f"{end_point}{sr_names}", headers=HEADERS, params=params).json()
            self.sr_list.extend(res['names'])
        return self.sr_list

