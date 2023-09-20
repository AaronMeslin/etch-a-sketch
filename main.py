#import all the modules needed for the feather and wings

import board
import displayio
import terminalio
import time
import adafruit_displayio_sh1107
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

#define each button with the const() function
#this code was provided from the Seesaw library
BUTTON_RIGHT = const(6)
BUTTON_DOWN = const(7)
BUTTON_LEFT= const(9)
BUTTON_UP = const(10)
BUTTON_SEL = const(14)
button_mask = const(
        (1<<BUTTON_RIGHT)
        | (1<<BUTTON_DOWN)
        | (1<<BUTTON_LEFT)
        | (1<<BUTTON_UP)
        | (1<<BUTTON_SEL)
)

#set up the display and board
displayio.release_displays()

i2c = board.I2C()
#i2c_bus = board.I2C()

#this code was provided by the SeeSaw library
display_bus = displayio.I2CDisplay(i2c,device_address=0x3C)
ss = Seesaw(i2c)

ss.pin_mode_bulk(button_mask, ss.INPUT_PULLUP)

#set values for the last input for the joystick
last_joy_x = 0
last_joy_y = 0


#current size for drawing
size_value =0
#width and height for the oled
WIDTH = 128
HEIGHT = 64
BORDER = 0

#set up display and color bitmap
display = adafruit_displayio_sh1107.SH1107(display_bus,width=WIDTH,height=HEIGHT,rotation=0)
splash=displayio.Group()
display.show(splash)
color_bitmap = displayio.Bitmap(128,64,2)


#create an all white background
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite=displayio.TileGrid(color_bitmap,pixel_shader=color_palette,x=0,y=0)
splash.append(bg_sprite)



#run while true
while True:
#    print("hello")
#    print(round(size_value))
    time.sleep(.1)
    #read anaglog joystick input
    current_joy_x = ss.analog_read(3)
    current_joy_y = ss.analog_read(2)

    #read input that is 0-1023 into 0-128 and 0-64
    draw_joy_x = round(current_joy_x/7.9921875)
    draw_joy_y = round(current_joy_y/15.984375)


    #read all current button input
    buttons = ss.digital_read_bulk(button_mask)
    #if only the A button is pressed
    if not buttons & (1<<BUTTON_RIGHT):
        try:
            for i in range(size_value):
                for k in range(size_value):

                    #if A is pressed, draw a square where the jotstick anaglogs are, the number of size value makes the squares bigger or smaller

                    #set each pixel in a square around the current selected pixel using joy sticks adding and subrating size value to create the right size, black sqaure
                    #using different signs and subtracting/adding the i and k, it goes through every pixel in the square for the pen to be drawn.
                    color_bitmap[draw_joy_x+round((i/2)),draw_joy_y+round((k/2))] = 1
                    color_bitmap[draw_joy_x-round((i/2)),draw_joy_y-round((k/2))] = 1
                    color_bitmap[draw_joy_x+round((i/2)),draw_joy_y-round((k/2))] = 1
                    color_bitmap[draw_joy_x-round((i/2)),draw_joy_y+round((k/2))] = 1
            #set current pixel what is selected with joys, black
            color_bitmap[draw_joy_x,draw_joy_y] = 1
            last_colored_x = draw_joy_x
            last_colored_y = draw_joy_y

        #if index error, which was occuring when parts of the square was out of bounds of the screen cordinates, ignore and fill the sqaure that is in bounds.
        except IndexError:
            pass

    #if B is pressed decrease size value
    if not buttons & (1<<BUTTON_DOWN):
        if size_value >= 0:
            size_value = size_value - .5
        else:
            size_value = 0

    #if y is pressed clear screen
    if not buttons & (1<<BUTTON_LEFT):
        for i in range(128):
            for k in range(64):
                color_bitmap[i,k]=0
        size_value = 0
    #if X is pressed increase size value
    if not buttons & (1<<BUTTON_UP):
        #only run if the size value is postitve, which lets it never go negative which would lead to a negative size square(not good)
        if size_value >= 0:
            size_value = size_value + .5


        else:
            size_value = 0
    if not buttons & (1<<BUTTON_SEL):
        pass
