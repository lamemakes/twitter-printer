from PIL import Image
from escpos.printer import Usb
import time
import json

# vend = 0x1504, prod = 0x003d
class TweetPrinter:
    def __init__(self, cfg):
        self.cfg = cfg

        self.p = Usb(
            idVendor=int(self.cfg.get("idVendor"), 16),
            idProduct=int(self.cfg.get("idProduct"), 16),
            out_ep=2
        )

    # Expects a tweet object containing something of the following:
    # {"username": "@testUser", "content": "This is a test tweet", "qr": "https://lamemakes.com", "pics": ["lamemakes.jpg"]}
    # Username & content are the only required fields.
    def printTweet(self, tweet):
        username = tweet.get("username")
        content = tweet.get("content")

        if tweet.get("error"):
            self.p.set(align="left", text_type=u'normal')
            self.p.text("@" + username + " caused an error:\n")
            self.p.set(align="center", text_type=u'b')
            self.p.text(content + "\n")
            self.p.text("Nice! You broke me...")
            self.p.cut()
            return

        # Print tweet username & content
        self.p.set(align="left", text_type=u'normal')
        self.p.text("@" + username + " tweeted:\n")
        self.p.set(align="center", text_type=u'b')
        self.p.text(content)

        # Print all tweet QR codes
        if tweet.get("qr"):
            self.printQR(tweet.get("qr"))

        # Print all tweet pics
        if tweet.get("pics"):
            for pic in tweet.get("pics"):  
                self.printImage(pic)
        
        # Print the footer
        if self.cfg.get("footerMessage") and self.cfg.get("footerMessage") != "":
            self.printFooter(self.cfg.get("footerMessage"))

        # Cut the paper
        self.p.cut()


    def printImage(self, filename):
        img = Image.open(filename).convert('RGB')
        format = filename.split(".")[-1]
        if format.upper() == "JPG":
            format = "JPEG"
        if img.width > 500:
            resized_img = img.resize((500, round((500 / img.width) * img.height)))
            resized_img.save(filename, format=format)
        self.p.image(filename)


    def printQR(self, text):
        self.p.qr(content=text, size=6)


    def printFooter(self, footerMsg):
        self.p.set(align="center", text_type=u'normal')
        self.p.text("\n" * 4)
        self.p.text(footerMsg)


if __name__ == "__main__":

    cfg = {
        'watchUser': '@lame_printer',
        'nastyWords': [],
        'footerMessage': 'lamemakes @ ROC Maker Faire 2022',
        'oledDisplay': True
    }

    tweet_printer = TweetPrinter(cfg)

    tweet = {
        "username" : "bingggus",
        "content" : "Call me McChicken bc I be on that bread",
        "error" : None
    }

    tweet_printer.printTweet(tweet)

    tweet = {
        "username" : "beanboy420",
        "content" : "where beans",
        "error" : None
    }

    tweet_printer.printTweet(tweet)
