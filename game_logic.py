# Game_logic

import pygame
from cleaning import clean_up_poop
from discipline import discipline_monster
from feeding import feed_monster, display_food  # Import display_food
import random
from movement import update_monster_movement  # Import the function
from boundary_restriction import restrict_to_background  # Import the function

def update_monster(monster, dt, screen):
    """
    Updates the monster's stats, handles pooping, and updates poop positions.
    """
    monster.update(dt)

    if monster.poop_timer > 0:
        monster.poop_timer -= 1
    else:
        from pooping import make_monster_poop
        make_monster_poop(monster)

    # --- Collision detection for poop and vomit ---
    background_rect = pygame.Rect(145, 370, 285, 70)  # Get the background rect

    for poop in monster.poop_list:
        if poop["rect"].colliderect(monster.image_rect):
            print("Monster collided with poop!")
            # Reverse direction to avoid poop
            monster.direction[0] *= -1  
            monster.direction[1] *= -1
        restrict_to_background(poop["rect"], background_rect)  # Restrict poop to background

    if monster.vomit_image:
        vomit_rect = monster.vomit_image.get_rect(topleft=monster.vomit_rect.topleft)  # Create a rect for vomit
        if vomit_rect.colliderect(monster.image_rect):
            print("Monster collided with vomit!")
            # Reverse direction to avoid vomit
            monster.direction[0] *= -1  
            monster.direction[1] *= -1
        restrict_to_background(vomit_rect, background_rect)  # Restrict vomit to background
        monster.vomit_rect = vomit_rect  # Update the vomit_rect

    # ... (rest of your code) ...
            
    update_monster_movement(monster, dt, screen)  # Call the movement update function

def decrease_weight(monster, amount=1):  # You can adjust the amount
    """Decreases the monster's weight, ensuring it doesn't go below base_weight."""
    monster.weight -= amount
    monster.weight = max(monster.base_weight, monster.weight)

def handle_button_click(monster, button_label, selected_item=None):
    """
    Handles the actions when a button is clicked, including feeding, playing,
    cleaning, disciplining, and medicating.
    """
    print(f"Button Clicked: {button_label}")

    if button_label == "Feed":
        from feeding import apple, cake, steak, burger  # Import your food instances
        food_choices = [apple, cake, steak, burger]  # Create a list of food choices
        food_to_feed = random.choice(food_choices)  # Choose a random food

        display_food(monster)
        feed_monster(monster, food_to_feed)  # Pass the food_to_feed argument

    elif button_label == "Play":
        monster.play()
        print(f"Monster played with. Happiness: {monster.happiness}")
    elif button_label == "Clean":
        clean_up_poop(monster)
    elif button_label == "Discipline":
        discipline_monster(monster)
    elif button_label == "Medic":
        if monster.is_sick:
            if selected_item == monster.illness:
                monster.is_sick = False
                monster.illness = None
                print(f"Cured {monster.name} of {selected_item}!")
            else:
                print(f"That medicine doesn't work for {monster.illness}!")
        else:
            print(f"{monster.name} is not sick!")
