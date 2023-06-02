from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

from time import sleep

class Calculator:
    def __init__(self, app: App, emulator: Emulator) -> None:
        self.app = app
        self.emulator = emulator

    def run(self) -> None:
        self.current_number = 0
        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda power=i: self.binary_input(power)

    def binary_input(self, power: int) -> None:
        self.current_number += 2 ** power
        self.emulator.leds[power].toggle()