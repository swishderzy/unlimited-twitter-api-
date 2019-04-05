import tweepy
import sys
import jsonpickle
import os
import dateutil.parser
import pandas as pd

# Replace the API_KEY and API_SECRET with your application's key and secret.

auth = tweepy.AppAuthHandler("ojMoFI4UrHGLXYmWk0cHD6DU5", "QHK1K9kL8jOtx8cNhk1dKUp7I8ZNJmS7q4SFBXXpKGx6OIrHDf")

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# Continue with rest of code

def twitter_search(q, max_tweets = 10000, lang = "en") :
    searchQuery = q  # this is what we're searching for
    maxTweets = max_tweets # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits


    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1
    all_tweets = list()
    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,since_id=sinceId, lang = lang)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), lang = lang)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,max_id=str(max_id - 1),since_id=sinceId, lang = lang)
            if not new_tweets:
                print("No more tweets found")
                break

            tweetCount += len(new_tweets)
            all_tweets.append(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    print ("Downloaded {0} tweets".format(tweetCount))

    all_tweets = [i for sublist in all_tweets for i in sublist]
    times = list()
    texts = list()
    followers = list()
    names = list()
    entities = list()
    locations = list()
    tweets_sources = list()
    tweets_sources_followers = list()
    for i in range(len(all_tweets)):
        times.append(dateutil.parser.parse(all_tweets[i]._json["created_at"]))
        texts.append(all_tweets[i]._json["text"])
        followers.append(all_tweets[i]._json["user"]["followers_count"])
        names.append(all_tweets[i]._json["user"]["screen_name"])
        entities.append(all_tweets[i]._json["entities"])
        locations.append(all_tweets[i]._json["user"]["location"])
        try:
            tweets_sources.append(all_tweets[i]._json["retweeted_status"]["user"]["screen_name"])
            tweets_sources_followers.append(all_tweets[i]._json["retweeted_status"]["user"]["followers_count"])
        except:
            tweets_sources.append("None")
            tweets_sources_followers.append(0)



    df = pd.DataFrame({"date" : times, "text" : texts, "followers" : followers, "name" : names, "entities" : entities, "location" : locations, "tweet_source" : tweets_sources, "tweet_source_followers" : tweets_sources_followers})

    return df



if __name__ == "__main__":
    twitter_search(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Done")