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
        self.dino_led.on()

        self.jump_timer = time()
        self.on_ground = True

        self.obstacles = []
        self.obstacle_timer = time()
        self.next_obstacle_time = uniform(1, 2)

        self.app.special_button.when_pressed = self.jump

    def run(self) -> None:
        self.running = True
        while self.running:
            if time() - self.jump_timer > 0.4:
                self.dino_led.on()
                self.on_ground = True

            if time() - self.obstacle_timer > self.next_obstacle_time:
                self.obstacle_timer = time()
                self.next_obstacle_time = uniform(0.7, 2)
                self.obstacles.append(13)

            for i in range(len(self.obstacles)):
                self.obstacles[i] -= 0.05
                index = ceil(self.obstacles[i])
                self.app.leds[index].on()
                if index < 13:
                    self.app.leds[index + 1].off()

                if index == 2 and self.on_ground:
                    print("AAAAAAAAAAA")

            for i in range(len(self.obstacles)):
                if self.obstacles[i] < 0:
                    self.obstacles.pop(i)
                    break

            sleep(0.01)

    def jump(self) -> None:
        if self.on_ground:
            self.jump_timer = time()
            self.dino_led.off()
            self.on_ground = False