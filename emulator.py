from __future__ import annotations

from pygame.math import Vector2 as VEC
from threading import Thread
import pygame

class Button:
    _current_pos = 70

    def __init__(self, emulator: Emulator, pin: int) -> None:
        self.emulator = emulator
        self.emulator.buttons.append(self)

        self.pos = VEC(self.__class__._current_pos, 230)
        self.rect = pygame.Rect(*self.pos, 80, 80)
        self.__class__._current_pos += 100

        self.pin = pin
        self.state = 0
        self.when_pressed = lambda: print("empty function")

    def press(self) -> None:
        self.state = 1
        print(f"Button {self.pin} on")
        self.when_pressed()

    def release(self) -> None:
        self.state = 0

    def toggle(self) -> None:
        self.state = not self.state
        if self.state:
            self.when_pressed()

    def update(self) -> None:
        for event in self.emulator.events:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.press()
                    elif event.button == 3:
                        self.toggle()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.release()

    def draw(self) -> None:
        pygame.draw.rect(self.emulator.screen, (200, 200, 200), (*self.pos, 80, 80))
        pygame.draw.circle(self.emulator.screen, (150 * self.state,) * 3, self.pos + VEC(40, 40), 30)

class LED:
    _current_pos = 1200

    def __init__(self, emulator: Emulator, pin: int) -> None:
        self.emulator = emulator
        self.emulator.leds.append(self)

        self.pos = VEC(self.__class__._current_pos, 100)
        self.__class__._current_pos -= 80

        self.pin = pin
        self.state = 0

    def on(self) -> None:
        self.state = 1

    def off(self) -> None:
        self.state = 0

    def toggle(self) -> None:
        self.state = not self.state

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pygame.draw.circle(self.emulator.screen, (150 + 100 * self.state, 0, 0), self.pos, 30)

class Emulator:
    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = 1400, 400
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.running = True
        self.events = {}

        self.leds = []
        self.buttons = []

    def run(self) -> None:
        while self.running:
            self.update()
            self.draw()

    def update(self) -> None:
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

        for button in self.buttons:
            button.update()
        for led in self.leds:
            led.update()

    def draw(self) -> None:
        self.screen.fill((230, 230, 230))

        for button in self.buttons:
            button.draw()
        for led in self.leds:
            led.draw()

        pygame.display.flip()