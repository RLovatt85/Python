import random
from pathlib import Path

import pygame

# Initialize pygame's audio mixer
pygame.mixer.init()

# Find dice.mp3 in the same folder as this Python file
sound_file = Path(__file__).parent / "dice.mp3"

# Adjust the sound effect volume
sound = pygame.mixer.Sound(sound_file)
sound.set_volume(0.3) # set to 30%


dice = ''

while dice != 'quit':

    dice = input("Which dice would you like to roll? 20, 12, 10, 8, 6 or 4 or 'quit' ").strip().lower()

    # Quit the program
    if dice == 'quit':
        break

    # Check whether the user entered a valid die
    if dice in {"20", "12", "10", "8", "6", "4"}:
        sound.play()

    # 20-sided die
    if dice == "20":
        result = random.randint(1, 20)

    # 12-sided die
    elif dice == "12":
        result = random.randint(1, 12)

    # 10-sided die
    elif dice == "10":
        result = random.randint(1, 10)

    # 8-sided die
    elif dice == "8":
        result = random.randint(1, 8)

    # 6-sided die
    elif dice == "6":
        result = random.randint(1, 6)

    # 4-sided die
    elif dice == "4":
        result = random.randint(1, 4)

    # Anything other than the valid dice
    else:
        print("Not a real die. \n")
        continue

    print ("You rolled a...", result)

    if result == 1:
        print ("Ouch")

    if result == 20:
        print ("Nat 20!  NICE!")