from datetime import datetime
import time
import twint
import logging
import json
import re
import os
import requests
import shutil

class TweetGetter:
    def __init__(self, cfg):
        # init loggers
        self.log = logging.getLogger()

        # Load the config.json
        self.cfg = cfg

        # Variables for the program

        # Checkout the watchUser variable, if None or "", exit program
        self.watch_user = self.cfg.get("watchUser")
        self.log.info("Twitter username to watch set to: " + self.watch_user)
        if not self.watch_user or self.watch_user == "":
            self.log.error("Twitter username not specified in config.json, exiting!")
            exit()
        
        self.tweets = []
        self.img_dir = "/etc/twitter_printer/images/"

    def getTweets(self, twint_conf, query):
        twint_conf.Search = query
        twint_conf.Pandas = True

        twint.run.Search(twint_conf)

        tweets_data_frame = twint.storage.panda.Tweets_df

        return tweets_data_frame.values.tolist()


    def getNewTweets(self):
        # Initialize twint and disable output
        twint_conf = twint.Config()
        twint_conf.Hide_output = True

        # Pull all mentions of "watchUser"
        all_mentions = self.getTweets(twint_conf=twint_conf, query=self.watch_user)

        new_tweets = []

        if len(all_mentions) > len(self.tweets):
            if len(self.tweets) > 0:
                self.log.debug("New tweets found!")

                # diff_tweet_list function is used because set() can't be used on a list that contains a list
                new_tweets = self.diff_tweet_list(all_mentions, self.tweets)
                self.tweets = self.tweets + new_tweets

            else:
                self.log.debug("No saved tweets, appending to list")
                new_tweets = all_mentions
                self.tweets = all_mentions

            return new_tweets
        
        # If no new tweets, return nothing
        return None


    # Pulled from https://www.scrapingbee.com/blog/download-image-python/
    def downloadPics(self, url, filename):

        pic_ext = url.split(".")[-1]

        res = requests.get(url, stream = True)

        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)

        if res.status_code == 200:
            with open(self.img_dir + filename + "." + pic_ext,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            self.log.info(filename + " sucessfully downloaded from " + url)
            return self.img_dir + filename + "." + pic_ext
        else:
            self.log.error(filename + " failed to downloaded from " + url)


    # Filter from a list of nasty terms that shouldn't be printer on paper, and format text. 
    def parseTweet(self, tweet):
        form_tweet = {}

        tweet_id = tweet[0]
        form_tweet["username"] = tweet[12]
        form_tweet["content"] = tweet[6]
        form_tweet["datetime"] = tweet[3]

        form_tweet["content"] = form_tweet["content"].replace("&amp;", "&")

        # Confirm time is valid
        if not self.time_check(form_tweet["datetime"]):
            return None

        # In my list, tasteful swearing is allowed, if not encouraged
        # but any anti-love will be burnt in this function
        nasty_words = self.cfg.get("nastyWords")

        for word in nasty_words:
            if word in form_tweet["content"]:
                self.log.warn("Nasty tweet found from " + form_tweet["username"] + "! Content: " + form_tweet["content"])
                return None
        
        form_tweet["content"] = form_tweet["content"].replace(self.watch_user + " ", "")

        if "qr(" in form_tweet["content"]:
            try:
                # Pull the qr command out and set it
                qr_link = re.search("qr\((.*)\)", form_tweet["content"]).group(1)
                form_tweet["qr"] = qr_link
                form_tweet["content"] = re.sub("qr\(.*\)", "", form_tweet["content"])
            except Exception as e:
                self.log.error(str(e))
                form_tweet["content"] = str(e)
                form_tweet["error"] = True
        
        if len(tweet[18]) > 0:

            if len(tweet[18]) > 3:
                # Limit printed pics to 3
                tweet_pic_links = tweet[18][:2]
            else:
                tweet_pic_links = tweet[18]
            
            tweet_pics = []

            iter = 1
            for pic in tweet_pic_links:
                filename = self.downloadPics(pic, tweet_id + "_" + str(iter))
                tweet_pics.append(filename)
                iter += 1

            form_tweet["pics"] = tweet_pics

            if "https://t.co" in form_tweet["content"]:
                form_tweet["content"] = re.sub("https:\/\/t.co.*\s*$", "", form_tweet["content"])
        
        try:
            self.log.info("New tweet from " + form_tweet["username"] + " found at " + form_tweet["datetime"] + " with content: \"" + form_tweet["content"] + "\"")
        except TypeError as e:
            self.log.error("Failed to log new tweet due to TypeError: \"" + str(e))

        return form_tweet


    # UTILS

    # Pulled from https://www.geeksforgeeks.org/python-difference-two-lists/, used to compared stored tweets and new tweets.
    def diff_tweet_list(self, li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif


    # Confirm at the tweet was made within 5 mins of current time, returns false if the date is too old
    # TODO: Implement timezone readouts
    def time_check(self, tweet_time):
        date, time = tweet_time.split(" ")
        year, month, day = date.split("-")
        hour, minute, second = time.split(":")

        # Give 5 min tolerence to tweet time
        if int(minute) >= 55:
            minute = (int(minute) + 5) - 60
            hour = int(hour) + 1
        else: 
            minute = int(minute) + 5

        return datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second)) > datetime.now()


if __name__ == "__main__":
    cfg = {'watchUser': '@lame_printer', 'nastyWords': [], 'footerMessage': 'lamemakes @ ROC Maker Faire 2022'} 
    tweetGetter = TweetGetter(cfg)

    while True:
        new_tweets = tweetGetter.getNewTweets()
        if new_tweets:
            for tweet in new_tweets:
                form_tweet = tweetGetter.parseTweet(tweet)
                if form_tweet:
                    print(str(form_tweet))
                    
        time.sleep(1)