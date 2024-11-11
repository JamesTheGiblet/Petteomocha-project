# sleeping.py 

import pygame

def put_monster_to_sleep(monster):
    """Puts the monster to sleep with a sleeping animation."""

    if not monster.is_sleeping:
        monster.is_sleeping = True
        print(f"Monster {monster.name} is now sleeping.")
        monster.image = pygame.image.load("sleeping.png")  

        # Calculate sleep duration based on energy level
        base_sleep_duration = 300  # Minimum sleep time
        energy_factor = (100 - monster.energy) / 100  # How tired the monster is (0 to 1)
        extra_sleep_duration = 300 * energy_factor  # Extra sleep based on tiredness
        sleep_duration = base_sleep_duration + extra_sleep_duration
        monster.sleep_timer = int(sleep_duration)  # Convert to integer
        
        monster.current_animation = "sleeping"  # Start the sleeping animation
        monster.animation_frame = 0

                # Check if the monster is being put to sleep at the same time as the previous day
        current_time = pygame.time.get_ticks()  # Get current game time in milliseconds
        if monster.last_sleep_time is not None:
            time_difference = abs(current_time - monster.last_sleep_time)
            if time_difference < (1000 * 60 * 60 * 2):  # Check if within 2 hours of the previous sleep time
                monster.consecutive_sleep_days += 1
            else:
                monster.consecutive_sleep_days = 0
        monster.last_sleep_time = current_time

    else:
        print(f"Monster {monster.name} is already sleeping!")
        # Optionally play a sound or show an animation
