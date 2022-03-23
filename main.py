import requests, os
from common_words import common_words

common_words = common_words
API_KEY = os.environ.get("API_KEY_NEWS")


word_dict = {}
with open("posts_and_comments.txt", 'r') as reddit_f:
    for line in reddit_f:
        word_list = line.replace('-','').replace('#','').replace(';','').replace('&','').replace(',','').replace('\'','').replace('.','').replace('’s','').lower().split()
        for word in word_list:
            if word not in word_dict:
                if len(word) > 3 and word not in common_words:
                    word_dict[word] = 1
                else:
                    continue
            else:
                word_dict[word] += 1





# print(common_words)





############this is an API to get the newss for the trend##########
def get_trend_news(trend):
    url = "https://newsapi.org/v2/everything"
    key = NEWS_API_KEY
    params={
        "q":trend,
        "apiKey":key,
            }

    request = requests.get(url=url,params=params)
    #print(request.status_code)
    # pprint.pprint(request.json())
    data = request.json()
    print(data)
    print(data['totalResults'],
          data['articles'][0]["title"],
          data['articles'][0]["description"],
          data['articles'][0]["content"])
###################################################################

for k, v in word_dict.items():
    if v > 10:
        common_words.append(k)
        print(k, v)
        get_trend_news(k)

