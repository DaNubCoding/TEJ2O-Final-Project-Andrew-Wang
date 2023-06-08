from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

from time import sleep, time
from random import uniform
from math import ceil

class DinoGame:
    def __init__(self, app: App, emulator: Emulator) -> None:
        print("Initializing dino game")
        self.app = app
        self.emulator = emulator

        self.dino_led = self.app.leds[2]

        self.app.special_button.when_pressed = self.start

    def run(self) -> None:
        self.running = True
        self.playing = False
        while self.running:
            while self.running and not self.playing:
                sleep(0.01)

            while self.running and self.playing:
                if time() - self.obstacle_timer > self.next_obstacle_time:
                    self.obstacle_timer = time()
                    self.next_obstacle_time = uniform(0.9, 2)
                    self.obstacles.append(13)

                for i in range(len(self.obstacles)):
                    index = ceil(self.obstacles[i])
                    self.app.leds[index].on()
                    if index < 13:
                        self.app.leds[index + 1].off()

                    self.obstacles[i] -= self.speed

                    if index == 2 and self.on_ground:
                        self.end()
                        # Must break, or else the loop will continue
                        # causing an index error as self.reset() will
                        # set self.obstacles to an empty list
                        break

                if time() - self.jump_timer > 0.5:
                    self.dino_led.on()
                    self.on_ground = True

                if self.obstacles and self.obstacles[0] <= -1:
                    self.obstacles.pop(0)
                    self.score += 1
                    self.app.leds[0].off()

                self.speed += 0.00001
                if self.speed > 0.15:
                    self.speed = 0.15

                sleep(0.01)

            # Early return if the game was forcefully ended
            if not self.running:
                return

            for _ in range(4):
                self.dino_led.on()
                sleep(0.25)
                self.dino_led.off()
                sleep(0.25)

            binary = bin(self.score)[2:]
            for i, digit in enumerate(binary[::-1]):
                if digit == "1":
                    self.app.leds[13 - i].on()

    def start(self) -> None:
        self.playing = True
        self.app.special_button.when_pressed = self.jump
        for led in self.app.leds:
            led.off()

        self.score = 0
        self.speed = 0.05
        self.jump_timer = time()
        self.on_ground = True
        self.obstacles = []
        self.obstacle_timer = time()
        self.next_obstacle_time = uniform(0.9, 2)

        self.dino_led.on()

    def jump(self) -> None:
        if self.on_ground:
            self.jump_timer = time()
            self.dino_led.off()
            self.on_ground = False

    def end(self) -> None:
        self.playing = False
        for led in self.app.leds:
            led.off()
        self.app.special_button.when_pressed = self.start