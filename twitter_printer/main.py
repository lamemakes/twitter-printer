import logging
import time
import os
import json
from twitter_printer.get_tweets import TweetGetter
# import twitter_printer.display_controller as display_controller
import twitter_printer.tweet_print as tweet_print


twit_print_path = "/etc/twitter_printer/"
os.makedirs(twit_print_path + "logging/", exist_ok=True)
os.makedirs(twit_print_path + "config/", exist_ok=True)

log = logging.getLogger()
FORMAT = '%(asctime)s %(pathname)s %(message)s'
logging.basicConfig(level=logging.INFO, filename="twitter_printer.log", format=FORMAT)

def config_init():
    template_config = {"watchUser" : "", "nastyWords" : [], "footerMessage" : "", "oledDisplay" : False}
    try:
        with open(twit_print_path + "config/config.json", "r+") as cfg_file:
            cfg = json.loads(cfg_file.read())
    except FileNotFoundError as e:
        with open(twit_print_path + "config/config.json", "w") as cfg_file:
            cfg_file.write(json.dumps(template_config, indent=2))

        log.error(str(e) + ", file \"config.json\" not found in path: \"" + os.path.abspath(__file__) + "\"! File has been created, please populate the fields!")
        exit()
    
    return cfg

def main(cfg):
    log.info("Initializing Twitter Printer!")
    tweetGetter = TweetGetter(cfg)

    while True:
        new_tweets = tweetGetter.getNewTweets()
        if new_tweets:
            for tweet in new_tweets:
                form_tweet = tweetGetter.parseTweet(tweet)
                if form_tweet:
                    log.info("Attempting to print tweet from " + form_tweet["username"])
                    tweet_print.printTweet(form_tweet, cfg)
                    
        time.sleep(1)

main(config_init())
