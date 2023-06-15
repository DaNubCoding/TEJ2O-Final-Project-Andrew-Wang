"""


Made by Andrew Wang
"""

# Import from other files
from emulator import LED, Button, Emulator
from calculator import Calculator
from visualizer import Visualizer
from dino_game import DinoGame
from threading import Thread
from timer import Timer

# App class that will handle all the main logic
class App:
    def __init__(self) -> None:
        self.emulator = Emulator()

        # The order of the pins corresponding to the physical order of the buttons and LEDs
        self.led_pin_order = [26, 19, 13, 6, 5, 11, 9, 10, 22, 27, 17, 4, 3, 2]
        self.button_pin_order = [21, 20, 16, 12, 7, 8, 25, 24, 23, 18]

        # Initialize all LEDs
        self.leds = [LED(self.emulator, pin) for pin in self.led_pin_order]

        # Initialize all buttons
        self.buttons = [Button(self.emulator, pin) for pin in self.button_pin_order]
        # The button that has special functionality
        self.special_button = Button(self.emulator, 15)
        # The button that will toggle between the four modes
        self.mode_button = Button(self.emulator, 14)

        # Initialize what the mode button does (move to the next mode)
        self.mode_button.when_pressed = self.next_mode

        # List of the modes in the order they will be toggled
        self.modes = [Calculator, Visualizer, DinoGame, Timer]
        # Index of the current mode
        self.mode_index = 0
        # Initialize the first mode: calculator
        self.mode = Calculator(self)

    # Method that starts the program
    def run(self) -> None:
        # Create a thread that will run the current mode, and start it
        Thread(target=self.run_modes, daemon=True).start()
        self.emulator.run()

    # Method that will run the logic of the current mode, this will run in a thread
    def run_modes(self) -> None:
        # Execute the logic of the current mode
        # Ensure the logic of the next mode gets executed when the mode switches
        while True:
            self.mode.run()

    def next_mode(self) -> None:
        # Increment the index of the current mode
        self.mode_index += 1
        # Wrap the index around to 0 if it exceeds 3
        self.mode_index %= len(self.modes)

        # Reset all buttons (except mode button) with empty functions
        for button in self.buttons:
            button.when_pressed = lambda: print("empty function")
        self.special_button.when_pressed = lambda: print("empty function")

        # Stop the execution of the current mode
        self.mode.running = False

        # Turn off all LEDs that might be on
        for led in self.leds:
            led.off()

        # Select the class of the new mode by index, and initialize it
        self.mode = self.modes[self.mode_index](self)

# Create and run the program
app = App()
app.run()