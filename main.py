"""


Made by Andrew Wang
"""

from gpiozero import Button, LED
from time import sleep

mode_button = Button(14)
special_button = Button(15)

button_pin_order = [18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
buttons = [Button(i) for i in button_pin_order]

led_pin_order = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
leds = [LED(i) for i in led_pin_order]

mode = 0
current_number = 0
other_number = 0

def toggle_mode():
    global mode
    mode += 1
    function = mode_functions[mode]
    function()

def binary_input(button: Button, power: int):
    global current_number
    current_number += 2 ** power
    leds[power].on()
    button.when_pressed = lambda: None

def reset_buttons():
    for i, button in enumerate(buttons):
        button.when_pressed = lambda power=i, button=button: binary_input(power, button)

def next_number():
    global current_number, other_number
    reset_buttons()
    other_number = current_number
    current_number = 0

def run_calculator():
    reset_buttons()

    special_button.when_pressed = next_number

def run_visualizer():
    pass

def run_dino_game():
    pass

def run_timer():
    pass

mode_functions = [run_calculator, run_visualizer, run_dino_game, run_timer]

mode_button.when_pressed = toggle_mode

running = True
while running:
    sleep(0.01)