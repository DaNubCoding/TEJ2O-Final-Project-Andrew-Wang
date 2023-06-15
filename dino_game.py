from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator import Emulator
    from main import App

from time import sleep, time
from random import uniform
from math import ceil

class DinoGame:
    def __init__(self, app: App) -> None:
        print("Initializing dino game")
        self.app = app

        # Create a shortcut reference to the LED that represents the dino
        self.dino_led = self.app.leds[2]

        # Initialize the special button to a function that starts the game
        self.app.special_button.when_pressed = self.start

    def run(self) -> None:

        # Main control boolean, determines if the entire subprogram is running or not
        self.running = True
        # Decides whether the actual game part is still running and the player hasn't lost yet
        self.playing = False

        # Main loop of the dino game
        while self.running:

            # Wait for either the subprogram to exit or the player to start the game
            while self.running and not self.playing:
                sleep(0.01)

            # Continuously run the game until either the subprogram exits or the player loses
            while self.running and self.playing:

                # If the time passed since the previous obstacle spawned is greater than the pre-determined time duration
                if time() - self.previous_obstacle_time > self.next_obstacle_interval:
                    # Reset the time the previous obstacle spawned to right now
                    self.previous_obstacle_time = time()
                    # Determine a new time duration before the next one spawns
                    self.next_obstacle_interval = uniform(0.9, 2)
                    # Add a new entry to the list of obstacle positions
                    self.obstacle_positions.append(13)

                # Iterate through all obstacle positions
                for i in range(len(self.obstacle_positions)):
                    # Determine the integer position of the obstacle
                    index = ceil(self.obstacle_positions[i])
                    # Use this int position to index the correct LED to display the obstacle, and turn it on
                    self.app.leds[index].on()

                    # If the LED being turned on is anything but the rightmost one, turn off the LED to the right of it
                    # Meaning that when the obstacle moves to the left by one, the previous LED would not stay on
                    if index < 13:
                        self.app.leds[index + 1].off()

                    # Move the obstacle position to the left by "speed"
                    self.obstacle_positions[i] -= self.speed

                    # If the position of the obstacle is at the position of the player
                    # AND the player is NOT jumping (on the ground)
                    if index == 2 and self.on_ground:
                        # End the game
                        self.end()

                # If the player has jumped up for more than 0.5 seconds
                if time() - self.jump_start > 0.5:
                    # Drop the player back down (i.e. turn the LED back on)
                    self.dino_led.on()
                    # NOTE: does self-explanatory like this need a special comment?
                    self.on_ground = True

                # If the obstacles list is not empty and the leftmost obstacle moves out of the display
                if self.obstacle_positions and self.obstacle_positions[0] <= -1:
                    # Remove the leftmost obstacle position
                    self.obstacle_positions.pop(0)
                    # Increase the score by one
                    self.score += 1
                    # Turn off the leftmost LED
                    self.app.leds[0].off()

                # Slowly increment the speed of the obstacles' approach
                self.speed += 0.00001
                # Cap the speed at 0.15
                if self.speed > 0.15:
                    self.speed = 0.15

                sleep(0.01)

            # Early return if the game was forcefully ended
            if not self.running:
                return

            # Turn off all LEDs
            for led in self.app.leds:
                led.off()

            # Flash the dino LED on and off 4 times to indicate death
            for _ in range(4):
                self.dino_led.on()
                sleep(0.25)
                self.dino_led.off()
                sleep(0.25)

            # Convert the score to binary
            binary = bin(self.score)[2:]
            # Loop through binary number in reverse
            for i, digit in enumerate(binary[::-1]):
                # If the digit is one, turn on the corresponding LED
                if digit == "1":
                    self.app.leds[13 - i].on()

    # Function to start/restart the game
    def start(self) -> None:

        # NOTE: If the use of "playing" has already been explained the first time it was initialized, does this line need to be explained?
        self.playing = True

        # Make the special button perform jump when pressed
        self.app.special_button.when_pressed = self.jump

        # Turn off all LEDs
        for led in self.app.leds:
            led.off()

        # Reset all values to their initial values
        self.score = 0
        self.speed = 0.05
        self.jump_start = time()
        self.on_ground = True
        self.obstacle_positions = []
        self.previous_obstacle_time = time()
        self.next_obstacle_interval = uniform(0.9, 2)

        # NOTE: Is this self-explanatory?
        self.dino_led.on()

    # Method that initiates the player jump
    def jump(self) -> None:
        # If the player is on the ground
        if self.on_ground:
            # Set the time started jumping to right now
            self.jump_start = time()
            # Turn off the dino LED to indicate a jump
            self.dino_led.off()
            # NOTE
            self.on_ground = False

    # Method that will end the game
    def end(self) -> None:
        # Set playing to false which will exit the dino game main loop
        self.playing = False

        # Turn off all LEDs
        for led in self.app.leds:
            led.off()

        # Set the special button to start the game again when pressed
        self.app.special_button.when_pressed = self.start