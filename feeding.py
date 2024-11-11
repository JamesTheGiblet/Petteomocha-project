# feeding.py 

import pygame
import random
from boundary_restriction import generate_position_within_background

# Food class with expanded attributes
class Food:
    def __init__(self, value, name="Food", type="normal", nutritional_value=5, taste="bland", effect=None):
        self.value = value
        self.name = name
        self.type = type
        self.nutritional_value = nutritional_value
        self.taste = taste
        self.effect = effect

# Food instances with different properties
apple = Food(10, "Apple", "healthy", nutritional_value=8, taste="sweet")
cake = Food(20, "Cake", "junk", nutritional_value=3, taste="sweet", effect="energizing")
steak = Food(30, "Steak", "healthy", nutritional_value=10, taste="savory")
burger = Food(25, "Burger", "junk", nutritional_value=2, taste="savory", effect="happy")
# ... (more food instances) ...

def feed_monster(monster, food_to_feed): 
    """
    Feeds the monster, increasing its hunger with a chance of vomiting if overfed.
    Also adjusts the monster's weight and other stats based on the food type.
    """

    if monster.hunger < 100:
        monster.current_animation = "eating"
        monster.animation_frame = 0
        monster.hunger += food_to_feed.value  # Use the food's value to increase hunger
        monster.hunger = min(100, monster.hunger)  # Ensure hunger doesn't exceed 100
        print(f"Fed {monster.name} {food_to_feed.name}! Hunger: {monster.hunger}")

        # --- Vomit logic ---
        if monster.hunger > 80 and random.random() < 0.2:  # Combined conditions
            monster.vomit_image = pygame.image.load("vomit.png")
        # Position vomit within the background area
            background_rect = pygame.Rect(145, 370, 285, 70)  # Define the background rect
            vomit_x, vomit_y = generate_position_within_background(monster.vomit_image.get_width(), monster.vomit_image.get_height(), background_rect)
            monster.vomit_rect = monster.vomit_image.get_rect(topleft=(vomit_x, vomit_y))

            monster.hunger = 0
            monster.happiness -= 20
            print(f"{monster.name} vomited!")

        # --- Adjust weight based on food type ---
        if food_to_feed.type == "healthy":
            monster.weight += 1
        elif food_to_feed.type == "junk":
            monster.weight += 3

        # --- Apply food effects ---
        if food_to_feed.effect == "energizing":
            monster.energy += 10
            monster.energy = min(100, monster.energy)
        elif food_to_feed.effect == "happy":
            monster.happiness += 15
            monster.happiness = min(100, monster.happiness)
        # ... (handle other effects) ...

        # Ensure weight doesn't exceed max_weight
        monster.weight = min(monster.max_weight, monster.weight)
        pygame.time.delay(500)
        monster.food_image = None
    else:
        print(f"{monster.name} is already full!")

def display_food(monster, image_path="burger.png"):
    """
    Displays the food image next to the monster.
    """

    food_image = pygame.image.load(image_path)
    food_x = monster.image_rect.left - food_image.get_width() - 10
    food_y = monster.image_rect.y
    monster.food_image = food_image
    monster.food_rect = food_image.get_rect(topleft=(food_x, food_y))
    
