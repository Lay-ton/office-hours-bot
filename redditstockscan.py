import praw
import os
import csv
import math
import keys
import tickers
import helpers
from praw.models import MoreComments


# Set reddits user creds
username = keys.REDDITUSER
password = keys.REDDITPASS

# Set reddit API keys
APPID = keys.APPID
APPSECRET = keys.APPSECRET


# This function needs to add any stock tickers seen in sentnce into into the mapOfStocks
# sentence- The sentence that needs to parsed which possibly contains any stock tickers
# mapOfStocks - The mapping between stock tickers and the number of times they appear
# allstocks- A map of all stock tickers
def addStocks(sentence, mapOfStocks, allstocks, rank):
    # This newRank serves to weight stocks appearing at the top higher
    newRank = rank
    if rank != 0 and rank != 1:
        newRank = 1 / math.log2(rank)
    else:
        newRank = 1
    # Split the sentence into words
    splits = sentence.split()
    # Loop through each word
    for word in splits:
        newWord = word
        # if the first letter of the word is a $ get rid of it
        if word[0:1] == "$":
            newWord = word[1:]
        # If the word is a ticker then add it to the mapOfStocks
        if allstocks.get(newWord) != None:
            if mapOfStocks.get(newWord) == None:
                mapOfStocks.update({newWord: newRank})
            else:
                mapOfStocks.update(
                    {newWord: mapOfStocks.get(newWord) + newRank})


# This function processes comments for the post that is passed in
# reddit- the reddit object which allows us to communicate with reddit
# post - The thread whose comments we want to get
# mapOfStocks - The mapping between stock tickers and the number of times they appear
# allstocks- A map of all stock tickers
def processComments(reddit, post, mapOfStocks, allStocks, i):
    # Go through each comment and make a call to the addStocks function
    submission = reddit.submission(str(post.id))
    for comment in submission.comments:
        if isinstance(comment, MoreComments):
            continue
        addStocks(comment.body, mapOfStocks, allStocks, i)


def runRedditScanner(subreddit, postType, time, comments, desc, size):

    debug = f"{subreddit} {postType} {time} {comments} {desc} {size}"
    print(debug)

    # The reddit object which allows us to communicate with Reddit
    reddit = praw.Reddit(client_id=APPID, client_secret=APPSECRET, password=password,
                         user_agent='stock-scanner-script by ' + username, username=username)

    # Creates a map and gets all tickers from nasdaq ftp directory
    mapOfStocks = {}
    allStocks = tickers.getNasdaqTickers()

    # Go through the subreddits and get the data
    posts = None
    subreddit = reddit.subreddit(subreddit)
    # get the posts based on the postTypes the user wants and the number they want.
    if postType == "hot":
        posts = subreddit.hot(limit=size)
    elif postType == "top":
        posts = subreddit.top(limit=size, time_filter=time)
    elif postType == "controversial":
        posts = subreddit.controversial(
            limit=size, time_filter=time)
    elif postType == "new":
        posts = subreddit.new(limit=size)
    else:
        posts = subreddit.rising(limit=size)

    i = 0
    # Go through each post and process the title. Do description and comments if necessary.
    for post in posts:
        addStocks(post.title, mapOfStocks, allStocks, i)
        # Process the description
        if desc:
            addStocks(post.selftext, mapOfStocks, allStocks, i)
        # Process the comments for the post
        if comments:
            processComments(reddit, post, mapOfStocks, allStocks, i)
        i = i + 1

    # Sort the values of the mapofstocks and go through and print all of them in order
    sortedVals = sorted(mapOfStocks.values(), reverse=True)
    seen = {}

    # initialize the seen array
    for key in mapOfStocks.keys():
        seen.update({key: False})

    response = f"Here are the results:\n"

    # Go through the sortedVals and print every ticker along with its value in order
    for i in sortedVals[:20]:
        for key in mapOfStocks.keys():
            if mapOfStocks.get(key) == i and seen.get(key) == False:
                print(key + ": " + str(i))
                a_str = f"{key}: {str(i)}\n"
                response += a_str
                seen.update({key: True})
                break

    print(response)
    print(len(response))
    results = helpers.chop(response)

    return results
