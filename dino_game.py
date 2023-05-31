# Imports
from gpiozero import LED, Button
from time import sleep, time
from random import uniform
from math import ceil
import sys

# Main class that handles all game logic
class DinoGame:
    def __init__(self, leds: list[LED], jump_button: Button) -> None:
        # Create a reference to the list of LEDs and the jump button
        self.leds = leds
        self.jump_button = jump_button

        # Create a shortcut reference to the LED that represents the dino
        self.dino_led = self.leds[2]

    # Utility method to turn all LEDs off
    def all_off(self) -> None:
        for led in self.leds:
            led.off()

    # Main method that runs the game
    def run(self) -> None:

        # Decides whether the game still running and the player hasn't lost yet
        self.playing = False

        # Main loop
        while True:

            # Set the special button to start the game again when pressed
            self.jump_button.when_pressed = self.start

            # Wait for the player to start the game
            while not self.playing:
                sleep(0.01)

            # Continuously run the game until the player loses
            while self.playing:

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
                    self.leds[index].on()

                    # If the LED being turned on is anything but the rightmost one, turn off the LED to the right of it
                    # Meaning that when the obstacle moves to the left by one, the previous LED would not stay on
                    if index < 13:
                        self.leds[index + 1].off()

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
                    self.on_ground = True

                # If the obstacles list is not empty and the leftmost obstacle moves out of the display
                if self.obstacle_positions and self.obstacle_positions[0] <= -1:
                    # Remove the leftmost obstacle position
                    self.obstacle_positions.pop(0)
                    # Increase the score by one
                    self.score += 1
                    # Turn off the leftmost LED
                    self.leds[0].off()

                # Slowly increment the speed of the obstacles' approach
                self.speed += 0.00001
                # Cap the speed at 0.15
                if self.speed > 0.15:
                    self.speed = 0.15

                sleep(0.01)

            self.all_off()

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
                    self.leds[13 - i].on()

    # Function to start/restart the game
    def start(self) -> None:

        self.playing = True

        # Make the special button perform jump when pressed
        self.jump_button.when_pressed = self.jump

        self.all_off()

        # Reset all values to their initial values
        self.score = 0                  # Keeps track of the number of obstacles passed
        self.speed = 0.05               # Store the speed of obstacles coming towards the dino
        self.jump_start = time()        # The last time the dino jumped
        self.on_ground = True           # Whether the dino is on the ground or not
        self.obstacle_positions = []    # List containing positions of all obstacles
        self.previous_obstacle_time = time()            # Last time an obstacle spawned
        self.next_obstacle_interval = uniform(1, 2)     # Time before next obstacle spawns
        self.minimum_interval = 1       # Minimum time before the next obstacle spawns

        self.dino_led.on()

    # Method that initiates the player jump
    def jump(self) -> None:

        # If the player is on the ground
        if self.on_ground:
            # Set the time started jumping to right now
            self.jump_start = time()
            # Turn off the dino LED to indicate a jump
            self.dino_led.off()
            self.on_ground = False

    # Method that will end the game
    def end(self) -> None:

        # Set playing to false which will exit the dino game main loop
        self.playing = False
        self.all_off()

# The order of the pins corresponding to the physical order of the LEDs
led_pin_order = [26, 19, 13, 6, 5, 11, 9, 10, 22, 27, 17, 4, 3, 2]
# Initialize all LEDs
leds = [LED(pin) for pin in led_pin_order]

# Initialize the buttons
jump_button = Button(21)
# Initialize the exit button
exit_button = Button(20)
exit_button.when_pressed = sys.exit

# Intialize and start the game
game = DinoGame(leds, jump_button)
game.run()