# sexy_data.py
import praw,traceback

username = "RepresentativeTry157"
clientid = "4nwd7dOyEzISgBBN803JQQ"
clientsecret = "5lAOuqqInPthlp9JS_qL_HQU6gAG2Q"

reddit = praw.Reddit(client_id=clientid,
                     client_secret=clientsecret,
                     user_agent='praw_tutorial (by {})'.format(username))
import requests
import requests

def get_pushshift_data(data_type="submission", **kwargs):
    """
    Gets data from the pushshift api.

    :data_type: 'submission' or 'comment'
    :kwargs: query parameters. The ** allows us to pass any number of keyword arguments

    :return: output in JSON format
    """

    base_url = "https://api.pushshift.io/reddit/search/{}/".format(data_type)

    request = requests.get(base_url, params=kwargs)

    if request.status_code != 200: # status == 200 means the request has succeeded
        raise Exception("HTTP Error code: {}".format(request.status_code))

    return request.json()['data']
# data = get_pushshift_data(q="hi",subreddit="sexy", size=2) # q is your query; maximum size is 1000
# data
from datetime import datetime
after_ts = int(datetime(2021, 1, 1).timestamp())
before_ts = int(datetime(2021, 1, 31).timestamp())
# print("After: {}, Before: {}".format(after_ts, before_ts))

# sexy_data = get_pushshift_data(q="sexy",subreddit="sexy", size=10000, sort='asc', sort_type='created_utc',
                                # after=after_ts, before=before_ts)
# print(sexy_data)
import pandas as pd
import time, datetime
sexy_dates = []
# print(len(sexy_data))
def coolTime(t):
    return datetime.datetime.fromtimestamp(t).strftime('%c')

#for entry in sexy_data.to_dict():
#    newEntry = {}
#    for key in entry:
#        if key == "created_utc":
#            newEntry["created_utc"]=datetime.datetime.fromtimestamp(entry["created_utc"]).strftime('%c')
#        else:
#            newEntry[key]=entry[key]
#       sexy_dates.append(newEntry)
def getData(**kwargs):
    d = {"size":100, "sort":'asc', "sort_type":'created_utc'}
    for k in d:
        kwargs[k] = d[k]
    return get_pushshift_data(**kwargs)

startDT = datetime.datetime(2021, 1, 1).timestamp()
finDT = datetime.datetime(2021, 1, 31).timestamp()
i=0
after_ts = int(startDT)
before_ts = int(finDT)
overall = 0
# go = True
# subreddits = ["teenagers","LosAngeles","boston","newyorkcity","usa","nyc"]

# SUBREDDITS FOR USA
subreddits = ["teenagers","LosAngeles","boston","newyorkcity","usa","nyc"]
# SUBREDDITS FOR AUSTRALIA
aus_subs = ["Auusieteens","sydney","melbourne","australia","brisbane"]


allSubs = {"us":subreddits,"australia":aus_subs}
us_seasons = {"summer":[datetime.datetime(2021, 6, 1).timestamp(),datetime.datetime(2021, 8, 31).timestamp()]}
us_seasons["winter"]=[datetime.datetime(2020, 12, 1).timestamp(),datetime.datetime(2021, 2, 27).timestamp()]
australia_seasons = {"winter":[datetime.datetime(2021, 6, 1).timestamp(),datetime.datetime(2021, 8, 31).timestamp()]}
australia_seasons["summer"]=[datetime.datetime(2020, 12, 1).timestamp(),datetime.datetime(2021, 2, 27).timestamp()]


# australia_seasons = us_seasons[::-1]
seasons = {}
seasons["australia"] = australia_seasons
seasons["us"] = us_seasons

# KEYWORDS TO SEARCH
keywords = ["sexy","horny","ass","pussy", "condom","sex","sexual"]
total = {}
# countries = ["australia","us"]
i = 0
for country in seasons:
    seasonT = seasons[country]
    total[country] = {}
    for season in seasonT:
        total[country][season] = 0
        # after_ts = int(australia_seasons[season][0])
        # before_ts = int(australia_seasons[season][1])
        after_ts = int(seasonT[season][0])
        before_ts = int(seasonT[season][1])
        # before_ts = int(australia_seasons[season][1])
        for sub in allSubs[country]:
            for key in keywords:

                go = True
                # print("BEFORE: SEASON:",season,"SUB:",sub,"KEYWORD:",key)
                # Search Reddit (api gives chuncks of 100 results)
                while go:
                    try:
                        # restart reddit:
                        # if i>0 and i%2 == 0:
                        #     reddit = praw.Reddit(client_id=clientid,
                        #                          client_secret=clientsecret,
                        #                          user_agent='praw_tutorial (by {})'.format(username))
                        #     print(f"{i}: reloading reddit",end="")
                        #     print("....")
                        i+=1
                        # sexy_data = getData(q='"sexy"',subreddit="teenagers", after=after_ts, before=before_ts)
                        print(after_ts,before_ts)
                        sexy_data = getData(q=key,subreddit = sub, after=after_ts, before=before_ts)
                        if len(sexy_data)>0:
                            df = pd.DataFrame(sexy_data)[['id','subreddit', 'title', 'selftext', 'permalink', 'created_utc', 'num_comments']]
                            lastFrame = df.iloc[-1:]["created_utc"].item()
                            after_ts = lastFrame
                            print(f"Length: {len(sexy_data)} After: {coolTime(after_ts)}, Before: {coolTime(before_ts)}")
                            print(df)
                            overall += len(sexy_data)
                            total[country][season] += len(sexy_data)
                        # print("TOTAL:",overall,"AFTER: SEASON:",season,"SUB:",sub,"KEYWORD:",key)
                        print("TOTAL:",overall,":::",country,season,sub,key)
                        # print("TOTAL:",overall,":::",country,season,sub,key)
                        # print("TOTAL:",overall,":::",country,season,sub,key)
                        # time.sleep(10)
                        #End of results
                        if len(sexy_data) < 100:
                            go = False
                    except :
                        traceback.print_exc()

print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# while go:
#     if True:
#         i+=1
#         # sexy_data = get_pushshift_data(q='"sexy"',subreddit="teenagers",
#         #                                 after=after_ts, before=before_ts)
#         sexy_data = get_pushshift_data(q='"sexy"',subreddit="teenagers",
#                                         after=after_ts, before=before_ts)
#
#         print(f"Length: {len(sexy_data)} After: {coolTime(after_ts)}, Before: {coolTime(before_ts)}")
#         df = pd.DataFrame(sexy_data)[['id','subreddit', 'title', 'selftext', 'permalink', 'created_utc', 'num_comments']]
#         lastFrame = df.iloc[-1:]["created_utc"].item()
#         print(df)
#         # print(("!"*30+"\n")*10,len(sexy_data))
#         after_ts = lastFrame
#         total+=len(sexy_data)
#         if len(sexy_data) < 100:
#             print("STOPing!!!!!!!!!!")
#             go = False
#     # except:
#     #     pass
print("Overall=",overall)
print(total)
