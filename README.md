# A Lame Twitter Printer

The lame twitter printer is a Raspberry Pi Zero W hacked onto a USB receipt printer, combined with twitter will print all tweets (and included static media) that are tweeted at it!

This project utilizes the [twint](https://github.com/twintproject/twint) Python library, allowing for seemingly unlimited, quick Twitter requests & queries, along with not requiring a login or authenicated API. Thanks, twint!

A fun program that I (lamemakes) will use at the Rochester Maker Faire 2022. Use the code for whatever you like!


## Hardware

What I used:
- Raspberry Pi Zero W
- Bixolon SRP-350PLUSIII receipt printer
- An I2C 128x64 OLED display
- A stripped down 12v-to-5v USB buck converter (to power the RPi)
- Custom 3D printed bracket to mount the hardware in the printer


## Installation

1. Connect the Raspberry Pi Zero W to the internet & enabled SSH. This can now be done headlessly via the RPi Imager (CTRL + Shift + X - thank me later).

2. Connect the Receipt Printer to the Pi via USB. In my development & testing, I used a Bixolon SRP-350PLUSIII.

3. SSH to the Pi & install the code:

    1. (Optional) Install the Adafruit OLED library ```sudo pip3 install git+https://github.com/adafruit/Adafruit_Python_SSD1306.git#egg=Adafruit_SSD1306```

    2. Install twitter-printer  ```sudo pip3 install git+https://github.com/lamemakes/twitter-printer.git#egg=twitter-printer```


## Configuration

Upon initial installation, run the package using:
```sudo python3 -m twitter-printer.main```

Obtain the vendor & product ID's of the USB printer via:
```lsusb```
The output should look something like the following:
```Bus 001 Device 002: ID 1504:003d Bixolon CO LTD SRP-350plusIII```
Where ```1504```is the Vendor ID, and ```003d```is the Product ID.


This will generate the configuration at ```/etc/twitter_printer/config/config.json ```, populate the needed fields accordingly:
- ```watchUser```: Username to monitor on twitter for new tweets. i.e., ```@lame_printer```would be used to watch for tweets containing such.
- ```nastyWords```: A list of terms that will filter out tweets if the tweet contains that word. Filter nasty words.
- ```footerMessage```: A message to be printed at the bottom of every tweet print, can be anything.
- ```oledDisplay```: A boolean value to enable/disable an OLED display output. False by default.
- ```idVendor```: The previously noted vendor ID.
- ```idProduct```: The previously noted product ID.


## Usage

The Twitter printer can be run using the command:
```sudo python3 -m twitter-printer.main```

Then, just tweet at your specified ```watchUser```! 
It can print images that are attached to tweets, and QR codes by encapsulating the desired QR link in parenthesis. Example: qr(www.lamemakes.com)


## NOTES:

- To run the printer on every boot & using debian, add the startup command to ```/etc/rc.local```
- The twitter-printer **_MUST_** be run as sudo/root. It won't (in my experience) have proper permissions to access the USB printer otherwise.
- This is a WIP, and although mostly done some spitshine will come in the following weeks ;)
- All logging output goes to ```/etc/twitter_printer/logging/twitter_printer.log```
- Package may/may not be uploaded to PyPi. Will be demand based

