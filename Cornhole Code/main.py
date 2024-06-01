# main.py
#
# This file uses a Raspberry Pi Pico to take input from 3 types of sensors: 
# IR emitter/receiver, vibration sensors and a photoresistor. It uses these
# sensor inputs to control a strip of WS2812B LEDs.
#
# Author:   Alex Savic
# Date:     01/18/24

from machine import Pin, ADC
import time
import os
from neopixel import Neopixel
import random

# Setting up pins
# Pico LED pin
led_pin = Pin(25, Pin.OUT)

# Photoresistor
photo_pin = ADC(28)

# Vibration
vibration1 = ADC(26)
vibration2 = ADC(27) 

# IR
reciever = Pin(1, Pin.IN)

# Initialize sensor values
IR_blocked = False
top_vibration = False
bottom_vibration = False
dark = False

#LED
numpix = 300
strip = Neopixel(numpix, 0, 0, "GRB")

off = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
teal = (0, 128, 128)
light_blue = (0, 255, 255)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
white = (255, 255, 255)
brown = (90, 50, 14)
pink = (255, 192, 203)

colors = [red, orange, yellow, green, teal, light_blue, blue, indigo, violet, pink]


# photoresistor
# Determines how dark it is using the analog voltage value from a photoresistor
# Arguments: None
# Returns: a boolean representing if sensor is triggered or not
def photoresistor():
    value = photo_pin.read_u16()
    print("Photoresistor: " + str(value))
    
    if (value > 65000):
        return True
    else:
        return False

# vibration
# Determines if there is vibration occuring 
# Arguments: None
# Returns: a boolean representing if a signal was triggered or not
def vibration():
    vibration1_val = vibration1.read_u16()
    vibration2_val = vibration2.read_u16()
    
    print("Vibration 1: " + str(vibration1_val))
    print("Vibration 2: " + str(vibration2_val))

    # Returns a boolean, one value for each sensor
    threshold = 780
    if (vibration1_val > threshold or vibration2_val > threshold):
        return True
    else:
        return False
        

# IR
# Determines if the IR receiver is picking up signals from the IR emitter
# Arguments: None
# Returns: a boolean representing if sensor is triggered or not
def IR():
    signal = reciever.value()
    if signal:
        print("IR not blocked")
        return False
    else:
        print("IR blocked")
        return True

# LED_check
# Calls functions to ligh tup the LED strip based on values of the sensors
# Arguments:
#   dark: boolean representing if it is dark or not
#   vibration: boolean represnting if the vibration sensor is triggered
#   IR_blocked: boolean representing if the IR path was blocked or not
# Returns: none
def LED_check(dark, vibration, IR_blocked):
    
    if IR_blocked:
        time.sleep(0.2)
        LED_IR()
    elif vibration:
        time.sleep(0.2)
        LED_vibrated()
    elif dark:
        time.sleep(0.2)
        LED_dark()
    else:
        time.sleep(0.2)
        LED_off()
        

# LED_off
# Turns the LED lights off
# Arguments: none
# Returns: none
def LED_off():
    strip.fill(off)
    strip.show()


# LED_dark
# Animates the LED lights when it is dark
# Arguments: none
# Returns: none
def LED_dark():
    strip.fill(orange)
    strip.show()

# LED_vibrated
# Animates the LED lights when the board vibrated
# Arguments: none
# Returns: none
def LED_vibrated():
    LED_whole_board_flash()
    

# LED_IR
# Animates the LED lights when the IR path is blocked
# Arguments: none
# Returns: none
def LED_IR():
    functions = [LED_explosion, LED_expansion, LED_color_chaser, LED_chaser, LED_strobe, LED_symmetric, LED_rainbow_cycle]
    animation_function = random.choice(functions)
    print(animation_function)
    animation_function()

# LED_top
# Turns on the LEDs on the top of the board
# Arguments: 
#       brightness: int representing the brightness to set the pixels at
#       color: color object with rgb values to set pixel color to
# Returns: none
def LED_top(brightness, color):
    strip.brightness(brightness)
    strip.set_pixel_line(84,116, color)
    strip.show()

# LED_left
# Turns on the LEDs on the left of the board
# Arguments: 
#       brightness: int representing the brightness to set the pixels at
#       color: color object with rgb values to set pixel color to
# Returns: none
def LED_left(brightness, color):
    strip.brightness(brightness)
    strip.set_pixel_line(118,182, color)
    strip.show()

# LED_left_middle
# Turns on the LEDs on the left middle diagonal of the board
# Arguments: 
#       brightness: int representing the brightness to set the pixels at
#       color: color object with rgb values to set pixel color to
# Returns: none
def LED_left_middle(brightness, color):
    strip.brightness(brightness)
    strip.set_pixel_line(185,232, color)
    strip.show()

# LED_circle
# Turns on the LEDs on the circle hole of the board
# Arguments: 
#       brightness: int representing the brightness to set the pixels at
#       color: color object with rgb values to set pixel color to
# Returns: none
def LED_circle(brightness, color):
    strip.brightness(brightness)
    strip.set_pixel_line(237,267, color)
    strip.show()

# LED_right_middle
# Turns on the LEDs on the right middle diagonal of the board
# Arguments: 
#       brightness: int representing the brightness to set the pixels at
#       color: color object with rgb values to set pixel color to
# Returns: none
def LED_right_middle(brightness, color):
    strip.brightness(brightness)
    strip.set_pixel_line(269,299, color)
    strip.set_pixel_line(0,14, color)
    strip.show()

# LED_right
# Turns on the LEDs on the right of the board
# Arguments: 
#       brightness: int representing the brightness to set the pixels at
#       color: color object with rgb values to set pixel color to
# Returns: none
def LED_right(brightness, color):
    strip.brightness(brightness)
    strip.set_pixel_line(19,82, color)
    strip.show()

# LED_expansion
# Animates an expansin on the board from the hole outward
# Arguments: none
# Returns: none
def LED_expansion():
    strip.fill(off)
    t_end_buildup = time.time() + 2
    t_end_explosion = t_end_buildup + 2

    brightness = 50

    # Randomly picks a color
    color = random.choice(colors)

    # Loop to do buildup
    while time.time() < t_end_buildup:
        # Light up circle and brighten it
        LED_circle(brightness, color)
        brightness += 10
        time.sleep(0.05)

        # If brightness becomes above max reset it
        if (brightness >= 200):
            brightness = 50
        
        strip.show()

    # Loop to do expansion
    left_pixel = 235
    right_pixel = 265
    brightness = 200
    while time.time() < t_end_explosion:
        LED_circle(brightness, color)
        strip.set_pixel_line(left_pixel, left_pixel + 2, color)
        strip.set_pixel_line(right_pixel - 2, right_pixel, color)

        # Advances the explosion and keeps pixels in bounds
        left_pixel -= 3
        right_pixel += 3
        right_pixel = right_pixel % numpix

        strip.show()
        
    LED_off()
        
        
        
# LED_explosion
# Animates an explosion on the board from the hole outward
# Arguments: none
# Returns: none
def LED_explosion():
    LED_off()
    t_end_buildup = time.time() + 2
    t_end_explosion = t_end_buildup + 2

    brightness = 50

    # Randomly picks a color
    color = random.choice(colors)

    # Loop to do buildup
    while time.time() < t_end_buildup:
        # Light up circle and brighten it
        LED_circle(brightness, color)
        brightness += 10
        time.sleep(0.05)

        # If brightness becomes above max reset it
        if (brightness >= 200):
            brightness = 50
        
        strip.show()

    # Set expansion parameters
    left_diag_pixel = 235
    right_diag_pixel = 265
    top_pixel = 100
    left_pixel = 132
    right_pixel = 68
    top_expansion = 0
    side_expansion = 0
    diagonal_expansion = 0
    expansion_rate = 7

    # Loop to do explosion
    brightness = 200
    while time.time() < t_end_explosion:
        
        LED_circle(brightness, color)
        
        # Explosion down the diagonals
        strip.set_pixel_line((left_diag_pixel - diagonal_expansion) % numpix, (left_diag_pixel + diagonal_expansion) % numpix, color)
        strip.set_pixel_line((right_diag_pixel - diagonal_expansion) % numpix, (right_diag_pixel + diagonal_expansion) % numpix, color)
        if ((right_diag_pixel + diagonal_expansion) > 300):
            strip.set_pixel_line(0, (right_diag_pixel + diagonal_expansion) % numpix, color)
 
        diagonal_expansion += expansion_rate
            
        # Explosion on the top
        if (diagonal_expansion >= 7):
            strip.set_pixel_line((top_pixel - top_expansion) % numpix, (top_pixel + top_expansion) % numpix, color)
            top_expansion += expansion_rate
            
        # Explosion on the sides
        if (diagonal_expansion >= 12):
            strip.set_pixel_line((left_pixel - side_expansion) % numpix, (left_pixel + side_expansion) % numpix, color)
            strip.set_pixel_line((right_pixel - side_expansion) % numpix, (right_pixel + side_expansion) % numpix, color)
            side_expansion += expansion_rate


        strip.show()
        
    LED_off()
    

# LED_color_chaser
# Animates the lights on the board to cycle through colors continuously 
# Arguments: none
# Returns: none
def LED_color_chaser():
    LED_off()
    t_end = time.time() + 5
    brightness = 200
    counter = 0

    # Define the color gradients
    gradients = [
        (red, orange),
        (orange, yellow),
        (yellow, green),
        (green, teal),
        (teal, light_blue),
        (light_blue, blue),
        (blue, indigo),
        (indigo, violet),
        (violet, pink),
        (pink, red)
    ]

    # Loop to do animation
    while time.time() < t_end:
        strip.brightness(brightness)

        for i in range(0, 299, 30):
            start_index = i // 30
            strip.set_pixel_line_gradient(i, i + 29, gradients[start_index][0], gradients[start_index][1])

        strip.rotate_right(counter)
        counter += 8
        counter = counter % numpix

        strip.show()
        
    LED_off()
    

# LED_chaser
# Animates the lights on the board to have multiple pixels run around the board
# Arguments: none
# Returns: none        
def LED_chaser():
    LED_off()
    t_end = time.time() + 5
    brightness = 200
    counter = 0

    # Randomly picks a way to rotate the pixel
    rotations = [strip.rotate_right, strip.rotate_left]
    rotation_function = random.choice(rotations)

    # Randomly picks a color
    color = random.choice(colors)

    # Loop to do animation
    strip.brightness(brightness)
    while time.time() < t_end:
        
        LED_off()
        
        # Sets 10 pixels on
        for i in range(10):
            strip.set_pixel(i*30, color)

        rotation_function(counter)
        counter += 2
        counter = counter % numpix

        strip.show()
        
    LED_off()
        
        

# LED_strobe
# Animates the lights on the board to have a strobe effect
# Arguments: none
# Returns: none   
def LED_strobe():
    LED_off()

    t_end = time.time() + 5
    brightness = 200

    # Randomly picks a color
    color = random.choice(colors)

    # Loop to do animation
    strip.brightness(brightness)
    while time.time() < t_end:
        # LED on
        strip.fill(color)
        strip.show()
        time.sleep(0.25)

        # LED off
        LED_off()
        strip.show()
        time.sleep(0.25)
        
    LED_off()
        

# LED_rainbow_cycle
# Animates the lights on the board to constantly cycle through hues
# Arguments: none
# Returns: none  
def LED_rainbow_cycle():
    #Random hue and random direction it shifts in
    hue = random.randint(0, 65535)
    direction = random.choice([-1, 1])
    strip.brightness(200)
    t_end = time.time() + 5
    
    while time.time() < t_end:

        color = strip.colorHSV(hue, 255, 255)
        strip.fill(color)
        strip.show()

        # Increment the hue for the next iteration
        hue = (hue + (direction*2000)) % 65536
        
    LED_off()
        

# LED_symmetric
# Animates the lights on the board to expand syyemtrically from the sides and
#   the diagonals of the board
# Arguments: none
# Returns: none          
def LED_symmetric():
   
    LED_off()
    start_time = time.time()
    duration = 2.5 
    brightness = 200
    expansion = 0

    # Randomly picks a color
    color = random.choice(colors)

    # Loop to do animation
    strip.brightness(brightness)
    while (time.time() - start_time) < duration:

        # Left
        strip.set_pixel_line(150 - expansion, 150 + expansion, color)
        # Right
        strip.set_pixel_line((51 - expansion) % numpix, 51 + expansion, color)
        # Left diagonal
        strip.set_pixel_line(209 - expansion, 209 + expansion, color)
        # Right diangonal
        if ((292 + expansion) < numpix):
            strip.set_pixel_line(292 - expansion, (292 + expansion), color)
        else:
            strip.set_pixel_line(292 - expansion, 299, color)
            strip.set_pixel_line(0, 0 + expansion - (299 - 292), color)

        strip.show()
        expansion += 2
        time.sleep(0.01)
        
    LED_off()
        


# LED_whole_board_flash
# Animates the lights on the whole board to flash on and off
# Arguments: none
# Returns: none
def LED_whole_board_flash():
    LED_off()
    time.sleep(0.2)
    brightness = 150

    # Randomly picks a color
    color = random.choice(colors)

    # Flash animation
    strip.brightness(brightness)
    strip.fill(color)
    strip.show()
    time.sleep(0.5)

    LED_off()
    time.sleep(0.15)
    


# Function to run IR and vibration functions
def run_sensors():
    global IR_blocked, vibrated, dark
    
    for i in range(100):
        # Only update sensor values if they are not already True
        if not IR_blocked:
            IR_blocked = IR()
        if not vibrated:
            vibrated = vibration()
        if not dark:
            dark = photoresistor()

        print("")
        time.sleep(0.001)
        

# Main loop
while True:
    IR_blocked = False
    vibrated = False
    dark = False

    led_pin.toggle()
    
    run_sensors()
    
    # Call LED_check with the collected sensor data
    LED_check(dark, vibrated, IR_blocked)