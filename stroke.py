import pygame

def stroke_monster(monster):
    """Strokes the monster, increasing happiness and bond."""
    print(f"Stroking {monster.name}...")

    # Increase happiness
    monster.happiness += 10
    monster.happiness = min(100, monster.happiness)

    # Increase bond
    monster.bond += 5
    monster.bond = min(100, monster.bond)
    print(f"Stroked! Happiness: {monster.happiness}, Bond: {monster.bond}")

    # --- Vary response based on mood and bond ---

    if monster.happiness > 80 and monster.bond > 80:
        # Very happy and high bond: More enthusiastic response
        stroke_animation = [
            pygame.image.load("very_happy_1.png"),  # Replace with your image filenames
            pygame.image.load("very_happy_2.png"),
            pygame.image.load("very_happy_3.png")
        ]
        monster.bounce_height = 20  # Higher bounce
        # ... (optionally play a more enthusiastic sound) ...

    elif monster.happiness > 50:
        # Happy: Normal response
        stroke_animation = [
            pygame.image.load("happy_1.png"),  # Replace with your image filenames
            pygame.image.load("happy_2.png"),
            pygame.image.load("happy_3.png")
        ]
        monster.bounce_height = 10
        # ... (optionally play a normal stroking sound) ...

    else:
        # Not very happy: Subdued response
        stroke_animation = [
            pygame.image.load("neutral_1.png"),  # Replace with your image filenames
            pygame.image.load("neutral_2.png")
        ]
        monster.bounce_height = 5  # Smaller bounce
        # ... (optionally play a subdued sound or no sound) ...

    # --- Apply the animation and bounce ---
    monster.current_animation = "stroking"
    monster.animations.animations["stroking"] = stroke_animation
    monster.animation_frame = 0
    monster.bounce_speed = 5  # You can adjust the speed
    monster.bounce_direction = -1  # Start by moving upwards