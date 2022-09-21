# A Lame Twitter Printer

The lame twitter printer is a Python program that when connected to a USB receipt printer & twitter will print
all tweets that are tweeted at it!

A fun program that I (lamemakes) will use a the Rochester Maker Faire 2022. Use the code for whatever you like!

## Installation

The code is packaged as a Python package, but is not yet up on PyPi. So for the time being, it can be installed using:

1. (Optional) Install the Adafruit OLED library ``` sudo pip3 install git+https://github.com/adafruit/Adafruit_Python_SSD1306.git#egg=Adafruit_SSD1306 ```

2. Install twitter-printer from the  ``` sudo pip3 install git+https://github.com/lamemakes/twitter-printer.git#egg=twitter-printer ```


## Configuration

Upon initial installation, run the package using:
``` sudo python3 -m twitter-printer.main ```

Obtain the vendor & product ID's of the USB printer via:
``` lsusb ```
The output should look something like the following:
``` Bus 001 Device 002: ID 1504:003d Bixolon CO LTD SRP-350plusIII ```
Where ``` 1504 ``` is the Vendor ID, and ```003d ``` is the Product ID.


This will generate the configuration at ``` /etc/twitter_printer/config/config.json ```, populate the needed fields accordingly:
- ```watchUser``` : Username to monitor on twitter for new tweets. i.e., ```@lame_printer``` would be used to watch for tweets containing such.
- ```nastyWords``` : A list of terms that will filter out tweets if the tweet contains that word. Filter nasty words.
- ```footerMessage``` : A message to be printed at the bottom of every tweet print, can be anything.
- ```oledDisplay``` : A boolean value to enable/disable an OLED display output. False by default.
- ```idVendor``` : The previously noted vendor ID.
- ```idProduct``` : The previously noted product ID.


## Usage

The Twitter printer can be run using the command:
``` sudo python3 -m twitter-printer.main ```


## NOTES:

- To run the printer on every boot & using debian, add the startup command to ```/etc/rc.local```
- The twitter-printer **_MUST_** be run as sudo/root. It won't (in my experience) have proper permissions to access the USB printer otherwise.
- This is a WIP, and although mostly done some spitshine will come in the following weeks ;)
- All logging output goes to ```/etc/twitter_printer/logging/twitter_printer.log```