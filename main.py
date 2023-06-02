"""


Made by Andrew Wang
"""

from emulator import LED, Button, Emulator
from calculator import Calculator
from time import sleep

class App:
    def __init__(self) -> None:
        self.emulator = Emulator()

        self.led_pin_order = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
        self.button_pin_order = [18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
        self.leds = [LED(self.emulator, pin) for pin in self.led_pin_order]
        self.buttons = [Button(self.emulator, pin) for pin in self.button_pin_order]
        self.mode_button = Button(self.emulator, 14)
        self.special_button = Button(self.emulator, 15)

        self.calculator = Calculator(self, self.emulator)

    def run(self) -> None:
        self.emulator.run()
        self.calculator.run()

app = App()
app.run()