# pooping.py 

import pygame
import random
from boundary_restriction import generate_position_within_background

def make_monster_poop(monster):
    """
    Makes the monster poop, displaying an image and playing a sound.
    Also, resets the poop timer and decreases hygiene.
    """

    print(f"Monster {monster.name} pooped!")

    # Load the poop image
    poop_image = pygame.image.load("poop.png")  

    # Get the monster's position (within the background area)
    background_rect = pygame.Rect(145, 370, 285, 70)  # Updated boundary
    poop_x, poop_y = generate_position_within_background(poop_image.get_width(), poop_image.get_height(), background_rect)
    poop_rect = poop_image.get_rect(midtop=(poop_x, poop_y))


    # Add the poop data to the poop list
    monster.poop_list.append({"image": poop_image, "rect": poop_rect, "y_speed": 0})

    # Play a sound effect (optional)
    # pygame.mixer.init()
    # poop_sound = pygame.mixer.Sound("poop_sound.wav")  # Replace with your sound file
    # poop_sound.play()

    # Reset the timer for the next poop
    monster.poop_timer = random.randint(600, 1800)  # Adjust the range as needed

    # Decrease hygiene 
    monster.hygiene -= 10  # Adjust the value as needed
    monster.hygiene = max(0, monster.hygiene)  # Ensure hygiene doesn't go below 0
    print(f"Hygiene decreased to: {monster.hygiene}")