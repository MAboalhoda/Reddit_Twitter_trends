import requests, os
from subreddits import Subreddit_Names

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
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

######################requesting data from the reddit API##########
end_point = 'https://oauth.reddit.com'


####will create a text file to save the post self text and the comment selftext

with open("posts_and_comments.txt", "w") as file:
    subreddits = Subreddit_Names().sr_names()
    results=[]
    for sub in subreddits:
        sr_search = f'/r/{sub}/hot'  # here is th targeted subreddit
        params = {'limit': 10}

        res = requests.get(f"{end_point}{sr_search}", headers=headers, params=params)
        results.append(res.json())

    post_extention = []  # in this list we will save the comment extentions
    for result in results:
        for post in result['data']['children']:
            if post['data']['selftext'] != '':
                try:
                    # add post title to the file
                    file.write(str(post['data']['title']))
                    # add psot selftext to the file
                    file.write(str(post['data']['selftext']))
                    # add the comemnt extention
                    post_extention.append(post['data']['permalink'][:-1])
                except UnicodeEncodeError:
                    continue
    # we will itterate in the comment extentions and fitch the comment data from the API
    for post in post_extention:
        comment_res = requests.get(f"{end_point}{post}", headers=headers).json()
    # in this nested loop we will itterate in the comments to get the comment info and add it to the file
    for comment in comment_res:
        for text in comment['data']['children']:
            try:
                print(text["data"]['selftext'])
                file.write(text['data']['selftext'])
            except KeyError:
                print(text["data"]["subreddit"]+" has no comments")
