# unlimited-twitter-api-


An unlimited twitter api, his features include:
- No limitations in number of requests.
- Output in clear and easy csv format.

## Dependencies:
- tweepy: pip install tweepy
- pandas, sys, jsonpickle, os, dateutil.

## how it works:

in shell command type:

### python path_to_twitter_searcher.py quest path_to_save_csv_file max_tweets language_of_tweets api_key api_secret

- quest: the term of the search.
- path_to_save_csv_file: the path to the output csv file, 
    if not "file_name.csv" included then it will create a name for you in the format: twitter_results_quest_language.csv
- max_tweets: maximum number of tweets to be retrieved.
- language_of_tweets: the original language of the tweets.
- api_key: the api key obtained from the twitter developpers account
- api_key: the api secret obtained from the twitter developpers account


#### To Do:
include other parameters in the results and input.
