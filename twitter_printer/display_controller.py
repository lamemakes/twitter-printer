# LOTS of code inspired/pulled from https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/stats.py

import time
import subprocess
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class OledController:
    def __init__(self, cfg):

        self.enabled = False
        self.cfg = cfg

        if self.cfg.get("oledDisplay") or self.cfg.get("oledDisplay") == "True":

            self.enabled = True

            import Adafruit_SSD1306

            # 128x32 display with hardware I2C:
            self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)


            # Initialize library, clear display
            self.disp.begin()
            self.disp.clear()
            self.disp.display()

            # Create blank image for drawing.
            # Make sure to create image with mode '1' for 1-bit color.
            width = self.disp.width
            height = self.disp.height
            self.image = Image.new('1', (width, height))
            self.image.rotate(180)

            # Get drawing object to draw on image.
            self.draw = ImageDraw.Draw(self.image)

            # Draw a black filled box to clear the image.
            self.draw.rectangle((0,0,width,height), outline=0, fill=0)

            # Draw some shapes.
            # First define some constants to allow easy resizing of shapes.
            padding = -2
            self.top = padding
            self.bottom = height-padding
            # Move left to right keeping track of the current x position for drawing shapes.
            self.x = 0


            # Load default font.
            self.font = ImageFont.load_default()

    # Method to flip the image & display
    def postDrawFormat(self):
        self.disp.image(self.image.rotate(180))
        self.disp.display()
    

    def displayReady(self):
        if self.enabled:
            self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
            ready_msg = "Awaiting new tweet..."
            self.draw.text((self.x, self.top), ready_msg,  font=self.font, fill=255)
            ready_msg = self.cfg.get("watchUser")
            self.draw.text((self.x, self.top + 8), ready_msg,  font=self.font, fill=255)
            ssid = subprocess.getoutput("iwgetid -r")
            self.draw.text((self.x, self.top + 16), "SSID: " + str(ssid),  font=self.font, fill=255)
            ip_address = subprocess.getoutput("hostname -I")
            self.draw.text((self.x, self.top + 24), "IP: " + str(ip_address),  font=self.font, fill=255)
            self.postDrawFormat()


    def displayPrintingNewTweet(self, twitter_user):
        if self.enabled:
            self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
            new_twit_msg = "Found new tweet"
            self.draw.text((self.x, self.top), new_twit_msg,  font=self.font, fill=255)
            new_twit_msg = "from " + twitter_user + "!"
            self.draw.text((self.x, self.top + 8), new_twit_msg,  font=self.font, fill=255)
            start_print_msg = "Printing tweet..."
            self.draw.text((self.x, self.top + 24), start_print_msg,  font=self.font, fill=255)
            self.postDrawFormat()


    def displayError(self):
        if self.enabled:
            self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
            new_err_msg = "An error occurred!"
            self.draw.text((self.x, self.top + 8), new_err_msg,  font=self.font, fill=255)
            log_err_msg = "Check logs for info..."
            self.draw.text((self.x, self.top + 16), log_err_msg,  font=self.font, fill=255)
            self.postDrawFormat()


if __name__ == "__main__":
    # Testing stuff
    import time 

    cfg = {
        'watchUser': '@lame_printer',
        'nastyWords': [],
        'footerMessage': 'lamemakes @ ROC Maker Faire 2022',
        'oledDisplay': True
    }

    newOled = OledController()
    newOled.displayReady()

    time.sleep(5)

    newOled.displayPrintingNewTweet("@big_lameo")