# Special imports to allow circular import type annotation
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

# Import from the python standard library
from time import sleep

# Class that will handle all logic of the calculator mode
class Calculator:
    def __init__(self, app: App) -> None:
        print("Initializing calculator")
        # Store a reference to the main app
        self.app = app

        # Store references to different LEDs for convenience sake
        self.operation_led = self.app.leds[0]       # LED that indicates plus/minus
        self.sign_led = self.app.leds[1]            # LED that indicates pos/neg
        self.number_leds = self.app.leds[2:][::-1]  # LEDs that represent binary numbers

        # Reset attributes, buttons, and LEDs to their initially required state
        self.reset()

    # Run the main loop of the calculator
    # This is actually not required in this mode, however it is here for
    # 1. Consistency's sake: all mode classes have a run function
    # 2. The App class will call `self.mode.run` for all modes, in order to
    # avoid either a crash or the need for a special check
    # 3. In order to be able to exit on demand (by setting self.running to False)
    def run(self) -> None:
        self.running = True
        while self.running:
            sleep(0.01)

    def swap_addition_subtraction(self) -> None:
        self.subtraction = not self.subtraction
        self.operation_led.toggle()

    def binary_input_1(self, power: int) -> None:
        self.current_binary[power] = not self.current_binary[power]
        self.number_leds[power].toggle()
        self.app.special_button.when_pressed = self.next_number

    def binary_input_2(self, power: int) -> None:
        self.current_binary[power] = not self.current_binary[power]
        self.number_leds[power].toggle()

    def next_number(self) -> None:
        for i, digit in enumerate(self.current_binary):
            self.number_1 += digit * 2 ** i
        print(f"Number 1 --> {self.number_1}")

        for led in self.number_leds:
            led.off()

        self.app.special_button.when_pressed = self.calculate
        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda power=9-i: self.binary_input_2(power)

        self.current_binary = [False] * 10

    def calculate(self) -> None:
        for i, digit in enumerate(self.current_binary):
            self.number_2 += digit * 2 ** i
        print(f"Number 2 --> {self.number_2}")

        for led in self.number_leds:
            led.off()

        if not self.subtraction:
            answer = self.number_1 + self.number_2
        else:
            answer = self.number_1 - self.number_2

        negative = answer < 0
        binary = bin(answer)[2:]
        for i, digit in enumerate(binary[::-1]):
            if digit == "1":
                self.number_leds[i].on()

        if negative:
            self.sign_led.on()

        self.app.special_button.when_pressed = self.reset

    # Reset attributes, buttons, and LEDs to their initially required state
    def reset(self) -> None:
        # Turn off all LEDs
        for led in self.app.leds:
            led.off()

        self.subtraction = False            # Stores the operation: plus(False)/minus(True)
        self.current_binary = [False] * 10  # List that stores the input binary number
        self.number_1 = 0                   # The first operand
        self.number_2 = 0                   # The second operand

        # Initialize functionality of buttons
        self.app.special_button.when_pressed = self.swap_addition_subtraction
        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda power=9-i: self.binary_input_1(power)