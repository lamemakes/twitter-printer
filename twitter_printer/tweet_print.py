from PIL import Image
from escpos.printer import Usb
import twitter_printer.display_controller as display_controller
import time
import json


p = Usb(0x1504, 0x003d, 0, out_ep=2)

oled_control = display_controller.OledController()
oled_control.displayReady()

# Expects a tweet object containing something of the following:
# {"username": "@testUser", "content": "This is a test tweet", "qr": "https://lamemakes.com", "pics": ["lamemakes.jpg"]}
# Username & content are the only required fields.
def printTweet(tweet, cfg):
    username = tweet.get("username")
    content = tweet.get("content")

    if tweet.get("error"):
        p.set(align="left", text_type=u'normal')
        p.text("@" + username + " caused an error:\n")
        p.set(align="center", text_type=u'b')
        p.text(content + "\n")
        p.text("Nice! You broke me...")
        p.cut()
        return

    oled_control.displayPrintingNewTweet(username)
    time.sleep(2) # Sleeps are just to allow the printing status screens to be seen [1]

    # Print tweet username & content
    p.set(align="left", text_type=u'normal')
    p.text("@" + username + " tweeted:\n")
    p.set(align="center", text_type=u'b')
    p.text(content)

    # Print all tweet QR codes
    if tweet.get("qr"):
        printQR(tweet.get("qr"))

    # Print all tweet pics
    if tweet.get("pics"):
        for pic in tweet.get("pics"):  
            printImage(pic)
    
    # Print the footer
    if cfg.get("footerMessage") and cfg.get("footerMessage") != "":
        printFooter(cfg.get("footerMessage"))

    # Cut the paper
    p.cut()

    time.sleep(1) # Sleeps are just to allow the printing status screens to be seen [2]
    oled_control.displayReady()


def printImage(filename):
    img = Image.open(filename).convert('RGB')
    format = filename.split(".")[-1]
    if format.upper() == "JPG":
        format = "JPEG"
    if img.width > 500:
        resized_img = img.resize((500, round((500 / img.width) * img.height)))
        resized_img.save(filename, format=format)
    p.image(filename)


def printQR(text):
    p.qr(content=text, size=6)


def printFooter(footerMsg):
    p.set(align="center", text_type=u'normal')
    p.text("\n" * 4)
    p.text(footerMsg)


if __name__ == "__main__":
    # Testing & stuff
    oled_control.displayReady()

    tweet = {
        "username" : "bingggus",
        "content" : "Call me McChicken bc I be on that bread",
        "error" : None
    }

    printTweet(tweet)

    tweet = {
        "username" : "beanboy420",
        "content" : "where beans",
        "error" : None
    }

    printTweet(tweet)
