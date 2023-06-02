from __future__ import annotations
from threading import Thread
from sys import stdout
import os

class Button:
    def __init__(self, emulator: Emulator, pin: int) -> None:
        emulator.buttons.append(self)
        self.pin = pin
        self.state = 0
        self.when_pressed = lambda: None

class LED:
    def __init__(self, emulator: Emulator, pin: int) -> None:
        emulator.leds.append(self)
        self.pin = pin
        self.state = 0

    def on(self) -> None:
        self.state = 1

    def off(self) -> None:
        self.state = 0

    def toggle(self) -> None:
        self.state = not self.state

class Emulator:
    def __init__(self) -> None:
        self.leds = []
        self.buttons = []

    def run(self) -> None:
        self.thread = Thread(target=self.update)
        self.thread.run()

    def update(self) -> None:
        while True:
            os.system("cls")
            for led in self.leds:
                stdout.write("O " if led.state else ". ")
            print()
            for button in self.buttons:
                stdout.write("_ " if button.state else "= ")
            print()
            n = input()
            try:
                n = int(n) - 1
            except ValueError:
                if n == "-":
                    n = 10
                elif n == "=":
                    n = 11
            if n == -1:
                n = 9
            self.buttons[n].state = not self.buttons[n].state
            self.buttons[n].when_pressed()