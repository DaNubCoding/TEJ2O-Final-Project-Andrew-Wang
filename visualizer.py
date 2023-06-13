from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

import pytweening as tween
from time import sleep

class Visualizer:
    def __init__(self, app: App, emulator: Emulator) -> None:
        print("Initializing visualizer")
        self.app = app
        self.emulator = emulator

        for led in self.app.leds:
            led.off()

        self.easing_functions = [
            tween.easeOutSine,
            tween.easeOutQuad,
            tween.easeOutCubic,
            tween.easeOutQuart,
            tween.easeOutQuint,
            tween.easeOutExpo,
            tween.easeOutCirc,
            tween.easeOutBack,
            tween.easeOutElastic,
            tween.easeOutBounce,
        ]

        self.selected = 0
        self.progress = 0

        for i, button in enumerate(self.app.buttons):
            button.when_pressed = lambda index=i: self.set_easing_function(index)
        self.app.special_button.when_pressed = self.play

    def run(self) -> None:
        self.running = True
        self.playing = False
        while self.running:
            while self.running and not self.playing:
                sleep(0.01)

            if self.running:
                easing_function = self.easing_functions[self.selected]

                for button in self.app.buttons:
                    button.when_pressed = lambda: print("empty function")

            while self.running and self.playing:
                linear_value = 0
                final_value = 0
                while self.running and self.playing and linear_value < 1.0:
                    final_value = easing_function(linear_value)
                    linear_value += 0.03
                    led_index = int(final_value * 12)
                    if led_index > 11:
                        led_index = 11
                    for led in self.app.leds:
                        led.off()
                    self.app.leds[led_index].on()
                    sleep(0.1)

            if self.running:
                for i, button in enumerate(self.app.buttons):
                    button.when_pressed = lambda index=i: self.set_easing_function(index)

    def set_easing_function(self, index: int) -> None:
        self.selected = index
        for led in self.app.leds:
            led.off()
        self.app.leds[index].on()
        print(f"Easing function --> {self.easing_functions[index].__name__}")

    def play(self) -> None:
        self.playing = True
        self.app.special_button.when_pressed = self.stop

    def stop(self) -> None:
        self.playing = False
        for led in self.app.leds:
            led.off()
        self.app.special_button.when_pressed = self.play