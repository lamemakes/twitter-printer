import logging
import time
import os
import json
from twitter_printer.get_tweets import TweetGetter
from twitter_printer.tweet_print import TweetPrinter
from twitter_printer.display_controller import OledController


twit_print_path = "/etc/twitter_printer/"
os.makedirs(twit_print_path + "logging/", exist_ok=True)
os.makedirs(twit_print_path + "config/", exist_ok=True)

log = logging.getLogger()
FORMAT = '%(asctime)s %(pathname)s %(message)s'
logging.basicConfig(level=logging.INFO, filename=twit_print_path + "logging/twitter_printer.log", format=FORMAT)

def config_init():

    template_config = {
        "watchUser" : "",
        "nastyWords" : [],
        "footerMessage" : "",
        "oledDisplay" : False,
        "idVendor" : None,
        "idProduct" : None
    }

    try:
        with open(twit_print_path + "config/config.json", "r+") as cfg_file:
            cfg = json.loads(cfg_file.read())
    except FileNotFoundError as e:
        with open(twit_print_path + "config/config.json", "w") as cfg_file:
            cfg_file.write(json.dumps(template_config, indent=2))

        log.error(str(e) + ", file \"config.json\" not found in path: \"" + os.path.abspath(__file__) + "\"! File has been created, please populate the fields!")
        exit()
    
    return cfg

def errorHandler(e_str):
    log.error(e_str)
    try:
        oled_control = OledController(config_init())
        oled_control.displayError()
    except Exception as e:
        # TODO: Should anything be done here?
        pass


def main(cfg):
    oled_control = OledController(cfg)
    try:
        log.info("Initializing Twitter Printer!")
        # Init tweet getter & printer
        tweet_getter = TweetGetter(cfg)
        tweet_print = TweetPrinter(cfg)

        while True:
            oled_control.displayReady()
            try:
                new_tweets = tweet_getter.getNewTweets()
                if new_tweets:
                    for tweet in new_tweets:
                        form_tweet = tweet_getter.parseTweet(tweet)
                        if form_tweet:
                            log.info("Attempting to print tweet from " + form_tweet["username"])
                            oled_control.displayPrintingNewTweet(form_tweet["username"])
                            time.sleep(2)
                            tweet_print.printTweet(form_tweet)
                            time.sleep(1)
            
                time.sleep(1)

            except Exception as e:
                log.error("Error in main loop: " + str(e))
    except Exception as e:
        log.error("Failed to start: " + str(e))



main(config_init())
