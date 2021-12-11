# sexy_data.py
import praw,traceback
import requests
from xo import *
# from pprint import pprint as pp

#
# username = "RepresentativeTry157"
# clientid = "4nwd7dOyEzISgBBN803JQQ"
# clientsecret = "5lAOuqqInPthlp9JS_qL_HQU6gAG2Q"

username = "RepresentativeTry157"
clientid = "7OvlNpQyE2zVBL5oYGrpiQ"
clientsecret = "jJqS4f7pkxQTrgFLCET5OJ3UCeyv-g"

def setupReddit():
    reddit = praw.Reddit(client_id=clientid,
                         client_secret=clientsecret,
                         user_agent='praw_tutorial (by {})'.format(username))
    return reddit
reddit = setupReddit()

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
    d = {"size":10000, "sort":'asc', "sort_type":'created_utc'}
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


def checkRelevance(post, keys):
    for key in keys:
        if key.lower() in str(post['title']).lower() + str(post['selftext']).lower():
            print(" !!!",str(post['title']).lower() + str(post['selftext']).lower())
            return True, key
    return False, None

def getPlaces():
    plist = "nyc","sydney","untited states","america","american","australia","australian","aussie"

    return plist
'''
::::::::::::::::::::
::: EXPERIMENT 2 :::
::::::::::::::::::::
'''
def filterDataFrames(data):
    dataframe,finalResults,season,current = data
    i =0
    for post in dataframe.iloc:
        i +=1
        # print(f"{i}/{len(list(dataframe.iloc))}")
        found, key = checkRelevance(post, getPlaces())
        if found:
            # current["data"].append([post,key])
            current["data"].append(post)
            # post["time"] = coolTime(post["created_utc"])
            # post["filter"] = key
            post["created_utc"] = coolTime(post["created_utc"])
            finalResults[season]["data"].append(post)

def experiment2():
    print("::: Running Experiment 2 :::")
    finalResults = {"total":0}
    places = getPlaces()

    '''
    # One Week #Year,Month,Day
    seasons = {"summer":[datetime.datetime(2021, 7, 1).timestamp(),datetime.datetime(2021, 7, 7).timestamp()]}
    seasons["winter"]=[datetime.datetime(2021, 1, 1).timestamp(),datetime.datetime(2021, 1, 7).timestamp()]
    # 2 Days #Year,Month,Day
    seasons = {"summer":[datetime.datetime(2021, 7, 1).timestamp(),datetime.datetime(2021, 7, 2).timestamp()]}
    seasons["winter"]=[datetime.datetime(2021, 1, 1).timestamp(),datetime.datetime(2021, 1, 2).timestamp()]
    # One Month
    seasons = {"summer":[datetime.datetime(2021, 7, 1).timestamp(),datetime.datetime(2021, 8, 1).timestamp()]}
    seasons["winter"]=[datetime.datetime(2021, 1, 1).timestamp(),datetime.datetime(2021, 2, 1).timestamp()]
    '''
    # Three Months
    seasons = {"summer":[datetime.datetime(2021, 6, 1).timestamp(),datetime.datetime(2021, 8, 31).timestamp()]}
    seasons["winter"]=[datetime.datetime(2020, 12, 1).timestamp(),datetime.datetime(2021, 2, 27).timestamp()]

    keywords = ["sexy","ass","pussy","horny","dick","condom","sex","sexual"]
    # How many subreddits to check, starting from the first
    subreddits = ["dating_advice","Tinder","HFY","teenagers","nyc","sydney"
    ,"ask","AskReddit","funny"
    ,"NoStupidQuestions","LifeProTips"
    ,"memes","gaming","motocycle"
    ,"SuccessionTV","femalefashionadvice","relationship_advice"]

    overwrite = False
    lastSub = xo.lastSub.value()
    if lastSub is None or lastSub < 1:
        lastSub = 1
        overwrite = True
    else:
        lastSub +=1
    subCount = lastSub
    xo.lastSub += 1
    # subCount = 1
    if subCount == len(subreddits):
        print("FINISHED ALL SUBREDDITS")
        xo.lastSub = 0
        return True
    print(f"CURRENT SUBREDDIT IS {subreddits[subCount-1:subCount]}")
    time.sleep(1)

    # Check for both seasons (Summer and Winter)
    for season in seasons:
        print(f"::: Searching Season {season} :::")
        # finalResults[season] = {"count":0}
        after_ts = int(seasons[season][0])
        original_ts = after_ts + 0
        before_ts = int(seasons[season][1])
        finalResults[season] = {"count":0,"subs":{},"data":[]}
        # Check every subreddit
        for sub in subreddits[subCount-1:subCount]:
            finalResults[season]["subs"][sub] = {"count":0,"data":[]}
            current = finalResults[season]["subs"][sub]
            go = True

            # This loops over time until results are none or final time was reached
            print(f"::: Searching {season} {sub} :::")
            while go:
                checking = f"checking between {coolTime(after_ts)} and {coolTime(before_ts)}"
                keys = "|".join(keywords[:])
                # Fetch Data From Reddit
                #Per Subreddit
                sexy_data = getData(q=keys,subreddit = sub, after=after_ts, before=before_ts)
                '''
                #All Reddit
                sexy_data = getData(q=keys, after=after_ts, before=before_ts)
                '''
                # If got data:
                if len(sexy_data)>0:
                    #Save data
                    dataframe = pd.DataFrame(sexy_data)[['id','subreddit', 'title', 'selftext', 'permalink', 'created_utc', 'num_comments']]
                    i=0
                    # Filter in another thread
                    filterAsync = True
                    if filterAsync:
                        xo.asyn(filterDataFrames,[dataframe,finalResults,season,current])
                    else:
                        for post in dataframe.iloc:
                            i +=1
                            # print(f"{i}/{len(list(dataframe.iloc))}")
                            found, key = checkRelevance(post, places)
                            if found:
                                current["data"].append(post)
                                # post["time"] = coolTime(post["created_utc"])
                                # post["filter"] = key
                                # post["created_utc"] = coolTime(post["created_utc"])
                                finalResults[season]["data"].append(post)


                    # current["data"].append(dataframe)

                    # Set the timeframe to start after the last result
                    lastFrame = dataframe.iloc[-1:]["created_utc"].item()

                    after_ts = lastFrame

                    # count results
                    finalResults["total"] += len(sexy_data)
                    finalResults[season]["count"] += len(sexy_data)
                    current["count"] += len(sexy_data)

                    # print results
                    fullscope = (before_ts - original_ts)
                    percent = ( fullscope - (before_ts - after_ts))/fullscope
                    print("\n"*3)
                    print(dataframe)
                    print(checking)
                    print(f"len(results):{len(sexy_data)}, keys:{keys[:2]}... subreddit:{sub} %{str(percent)[2:4]}")
                    print(f"len(filter):{len(current['data'])}, keys:{keys[:2]}... subreddit:{sub} %{str(percent)[2:4]}")
                    print(f"{season}:{sub}:count:{current['count']}")
                else:
                    print("Got no data .....................")

                if len(sexy_data) < 90:
                    # print("FINISHING ",season,keys)
                    go = False
            print(f"Sub Finished...:{sub} count:{current['count']}")
            print(f" !!! {season} so far count:{finalResults[season]['count']}")
            reload = False
            if reload:
                print("""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%""")
                time.sleep(5)
                reddit = setupReddit()
                print("""%%%%%%%% Reloading Reddit %%%%%%%%%%""")
                time.sleep(10)
                print("""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%""")

        print(f" !!! Finished {season} count:{finalResults[season]['count']}")
    print(f" !!! Finished Experiment !!!")
    time.sleep(5)
    print(f"Total: {finalResults['total']}")
    print(f"Summer: {len(finalResults['summer']['data'])} / {finalResults['summer']['count']}")
    print(f"Winter: {len(finalResults['winter']['data'])} / {finalResults['winter']['count']}")
    if overwrite:
        xo.sexyData.summer = []
        xo.sexyData.winter = []
        time.sleep(3)

    finalSub = subreddits[subCount-1:subCount][0]
    prevSummer = xo.sexyData.summer.value()
    prevWinter = xo.sexyData.winter.value()
    if prevSummer is not None and len(prevSummer) > 0:
        print("Summer Previous:",len(prevSummer))
        prevSummer += finalResults['summer']['data']
    else:
        prevSummer = finalResults['summer']['data']

    if prevWinter is not None and len(prevWinter) > 0:
        print("Winter Previous:",len(prevWinter))
        prevWinter += finalResults['winter']['data']
    else:
        prevWinter = finalResults['winter']['data']

    xo.sexyData.summer = prevSummer
    xo.sexyData.winter = prevWinter

    fullSummer = pd.DataFrame(prevSummer)[['id','subreddit','created_utc', 'title', 'selftext', 'permalink', 'num_comments']]
    fullWinter = pd.DataFrame(prevWinter)[['id','subreddit','created_utc', 'title', 'selftext', 'permalink', 'num_comments']]

    # fullSummer.to_csv(f"summer_{finalSub}.csv")
    # fullSummer.to_csv(f"winter_{finalSub}.csv")
    fullSummer.to_csv(f"summer.csv")
    fullWinter.to_csv(f"winter.csv")

    print("::: SAVED TO XO :::")
    for sub in subreddits[subCount-1:subCount]:
        subTotal = 0
        for season in seasons:
            subTotal += finalResults[season]["subs"][sub]["count"]
        print(f"   r/{sub}:{subTotal}")

    # pp(finalResults)

#Run experiment2
experiment2()



'''
::::::::::::::::::::
::: EXPERIMENT 1 :::
::::::::::::::::::::
'''

ies = ["australia","us"]

def experiment1():

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
    # countr

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

# Run Experiment1
# experiment1()
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("XXXXXXXXXXXXXX FINISHED XXXXXXXXXXXXXX")
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
# print("Overall=",overall)
# print(total)
