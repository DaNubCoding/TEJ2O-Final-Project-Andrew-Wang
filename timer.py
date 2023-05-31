from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

from time import sleep, time

class Timer:
    def __init__(self, app: App) -> None:
        print("Initializing timer")
        self.app = app
        self.number_leds = self.app.leds[::-1]

        self.reset()

    def run(self) -> None:
        self.running = True
        self.started = False
        while self.running:
            while self.running and not self.started:
                sleep(0.01)

            while self.running and self.started and self.total_seconds != 0:
                self.progress = 1 - (time() - self.start_time) / self.total_seconds
                for i, led in enumerate(self.app.leds):
                    if i < self.progress * 14:
                        led.on()
                    else:
                        led.off()

                if self.progress < 0:
                    self.started = False

            if self.running:
                self.app.special_button.when_pressed = self.cancel

            while self.running and not self.canceled:
                for led in self.app.leds:
                    led.on()
                sleep(0.3)
                for led in self.app.leds:
                    led.off()
                sleep(0.3)

            if self.running:
                self.reset()

    def input_binary(self, power: int) -> None:
        self.current_binary[power] = not self.current_binary[power]
        self.number_leds[power].toggle()

    def next_number(self) -> None:
        for i, digit in enumerate(self.current_binary):
            self.minutes += digit * 2 ** i
        print(f"Minutes --> {self.minutes}")

        for led in self.number_leds:
            led.off()

        self.app.special_button.when_pressed = self.start_timer

        self.current_binary = [False] * 10

    def start_timer(self) -> None:
        for i, digit in enumerate(self.current_binary):
            self.seconds += digit * 2 ** i
        print(f"Seconds --> {self.seconds}")

        for led in self.number_leds:
            led.on()

        self.total_seconds = self.minutes * 60 + self.seconds
        self.progress = 1
        self.started = True
        self.start_time = time()
        self.canceled = False

        self.app.special_button.when_pressed = self.reset

    def cancel(self) -> None:
        self.canceled = True

    def reset(self) -> None:
        for led in self.app.leds:
            led.off()

        self.current_binary = [False] * 10
        self.minutes = 0
        self.seconds = 0
        self.started = False

        self.app.special_button.when_pressed = self.next_number
        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda power=9-i: self.input_binary(power)