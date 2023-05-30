"""


Made by Andrew Wang
"""

from gpiozero import Button, LED
from time import sleep

mode_button = Button(14)
special_button = Button(15)

button_pin_order = [21, 20, 16, 12, 7, 8, 25, 24, 23, 18]
buttons = [Button(i) for i in button_pin_order]

led_pin_order = [26, 19, 13, 6, 5, 11, 9, 10, 22, 27, 17, 4, 3, 2]
leds = [LED(i) for i in led_pin_order]

mode = 0

def run_calculator():
    pass

def run_visualizer():
    pass

def run_dino_game():
    pass

def run_timer():
    pass

running = True
while running:
    sleep(0.01)