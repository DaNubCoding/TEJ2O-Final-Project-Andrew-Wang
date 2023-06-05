from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

from time import sleep

class Calculator:
    def __init__(self, app: App, emulator: Emulator) -> None:
        print("Initializing calculator")
        self.app = app
        self.emulator = emulator

        for led in self.app.leds:
            led.off()

        self.subtraction = False
        self.current_binary = [False] * 10
        self.number_1 = 0
        self.number_2 = 0

        self.app.special_button.when_pressed = self.swap_addition_subtraction
        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda power=9-i: self.binary_input_1(power)

    def run(self) -> None:
        self.running = True
        while self.running:
            sleep(0.01)

    def swap_addition_subtraction(self) -> None:
        self.subtraction = not self.subtraction
        self.emulator.leds[-1].toggle()

    def binary_input_1(self, power: int) -> None:
        self.current_binary[power] = not self.current_binary[power]
        self.emulator.leds[power].toggle()
        self.app.special_button.when_pressed = self.next_number

    def binary_input_2(self, power: int) -> None:
        self.current_binary[power] = not self.current_binary[power]
        self.emulator.leds[power].toggle()

    def next_number(self) -> None:
        for i, digit in enumerate(self.current_binary):
            self.number_1 += digit * 2 ** i

        for led in self.app.leds[:-1]:
            led.off()

        self.app.special_button.when_pressed = self.calculate
        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda power=9-i: self.binary_input_2(power)

    def calculate(self) -> None:
        for i, digit in enumerate(self.current_binary):
            self.number_2 += digit * 2 ** i

        for led in self.app.leds[:-1]:
            led.off()

        print(self.number_1, self.number_2)