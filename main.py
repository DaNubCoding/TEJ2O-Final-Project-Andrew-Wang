"""


Made by Andrew Wang
"""

from emulator import LED, Button, Emulator
from calculator import Calculator
from threading import Thread
from time import sleep

class App:
    def __init__(self) -> None:
        self.emulator = Emulator()

        self.led_pin_order = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
        self.button_pin_order = [21, 20, 16, 12, 7, 8, 25, 24, 23, 18]

        self.leds = [LED(self.emulator, pin) for pin in self.led_pin_order]

        self.buttons = [Button(self.emulator, pin) for pin in self.button_pin_order]
        self.mode_button = Button(self.emulator, 14)
        self.special_button = Button(self.emulator, 15)

        self.special_button.when_pressed = self.next_mode

        self.modes = [Calculator]
        self.mode_index = 0
        self.mode = Calculator(self, self.emulator)

    def run(self) -> None:
        Thread(target=self.run_modes, daemon=True).start()
        self.emulator.run()

    def run_modes(self) -> None:
        while True:
            self.mode.run()

    def next_mode(self) -> None:
        self.mode_index += 1
        self.mode_index %= len(self.modes)
        self.mode = self.modes[self.mode_index](self, self.emulator)

app = App()
app.run()