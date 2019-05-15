# This is designed so you can place your ACPE on your Roomba vacuum and play different sounds when the device bumps into an obstacle.
# You can use the A and B buttons to adjust the sensitivity. Load and reference different sounds as you see fit.

import time
import random
import microcontroller 
from adafruit_circuitplayground.express import cpx

# Set this as a float from 0 to 1 to change the brightness. The decimal represents a percentage.
# So, 0.3 means 30% brightness!  Minimum that seems to still display all colors = 0.07
cpx.pixels.brightness = 0.07

# Changes to NeoPixel state will not happen without explicitly calling show()
cpx.pixels.auto_write = False

show_color_wheel = True

#List of the random sounds generated when a tap or shock is detected
sounds = []
sounds.append("MarioLevelUp.wav")
sounds.append("MarioCoin.wav")
sounds.append("Hold_on.wav")
sounds.append("Wilhelm.wav")
sounds.append("MarioJump.wav")


def color_wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition red - green - blue - back to red.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int(255 - pos*3), int(pos*3), 0)
    if pos < 170:
        pos -= 85
        return (0, int(255 - pos*3), int(pos*3))
    pos -= 170
    return (int(pos * 3), 0, int(255 - (pos*3)))

def show_pixels(max_pos, r, g, b):
    #Iterate through the pixels and apply the color
    color = (r, g, b)
    cpx.pixels.fill((0,0,0))
    for i in range(max_pos):
        cpx.pixels[i] = color 
        cpx.pixels.show()

color_index = 0
pixel_number = 0
shock_level = 10
shock_max = 25

cpx.play_file("Hold_on.wav")  #Startup greeting

# time.monotonic() allows for non-blocking LED animations!
start = time.monotonic()
while True:
    now = time.monotonic()
    if show_color_wheel:
        # Red-comet rainbow swirl!
        pixel_number = (pixel_number + 1) % 10
        for p in range(10):
            color = color_wheel(25 * ((pixel_number + p) % 10))
            cpx.pixels[p] = tuple([int(c * (10 - (pixel_number + p) % 10) / 10.0) for c in color])
            cpx.pixels.show()

    # If the switch is to the left, it returns True AND both the shock and the tap sensor are enabled : Untested
    cpx.red_led = cpx.switch
    cpx.detect_taps = cpx.switch

    # Press the buttons to adjust the skock sensitivity and then briefly display the sensitivity dial in blue
    if cpx.button_a:
        shock_level -= 1 # More sensitive to shock
        cpx.play_file("MarioCoin.wav")
        if shock_level < 2:
            shock_level = 1
        show_pixels((10 * shock_level // shock_max)-1, 0, 0, 255)
    elif cpx.button_b:
        shock_level += 1 # Less sensitive to shock
        cpx.play_file("MarioCoin.wav")
        if shock_level > shock_max:
            shock_level = shock_max
        show_pixels((10 * shock_level // shock_max)-1, 0, 0, 255)

    if cpx.tapped: 
        cpx.pixels.fill((0, 255, 0)) #Show Green to indicate "Tapped" triggered
        cpx.pixels.show()
        cpx.play_file(sounds[random.randint(0,len(sounds)-1)])
        show_pixels(10, 0, 0, 0)

    if cpx.shake(shake_threshold=shock_level):
        cpx.pixels.fill((255, 0, 0)) #Show Red to indicate "Skake" triggered
        cpx.pixels.show()
        cpx.play_file(sounds[random.randint(0,len(sounds)-1)])
        show_pixels(10, 0, 0, 0)

