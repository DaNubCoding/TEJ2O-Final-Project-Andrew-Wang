"""


Made by Andrew Wang
"""

from gpiozero import LED, Button
from calculator import Calculator
from visualizer import Visualizer
from dino_game import DinoGame
from threading import Thread
from timer import Timer

from time import sleep

class App:
    def __init__(self) -> None:
        self.led_pin_order = [26, 19, 13, 6, 5, 11, 9, 10, 22, 27, 17, 4, 3, 2]
        self.button_pin_order = [21, 20, 16, 12, 7, 8, 25, 24, 23, 18]
        # 16 

        self.leds = [LED(pin) for pin in self.led_pin_order]

        self.buttons = [Button(pin) for pin in self.button_pin_order]
        self.special_button = Button(15)
        self.mode_button = Button(14)

        self.mode_button.when_pressed = self.next_mode

        self.modes = [Calculator, Visualizer, DinoGame, Timer]
        self.mode_index = 0
        self.mode = Calculator(self)

    def run(self) -> None:
        # Thread(target=self.run_modes, daemon=True).start()
        # self.emulator.run()
        while True:
            self.mode.run()

    def run_modes(self) -> None:
        while True:
            self.mode.run()

    def next_mode(self) -> None:
        self.mode_index += 1
        self.mode_index %= len(self.modes)

        for button in self.buttons:
            button.when_pressed = lambda: print("empty function")
        self.special_button.when_pressed = lambda: print("empty function")

        self.mode.running = False

        for led in self.leds:
            led.off()

        self.mode = self.modes[self.mode_index](self)

app = App()
app.run()