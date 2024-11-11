import pygame
import random
from evolution import Evolution  # Import the Evolution class
from animations import MonsterAnimations  # Import the MonsterAnimations class


class Monster:
    """Represents the virtual pet monster."""

    # Egg States
    EGG_IDLE = "egg_idle"
    EGG_SHAKE_1 = "egg_shake_1_of_2"
    EGG_SHAKE_2 = "egg_shake_2_of_2"
    EGG_HATCHING = "egg_hatching"
    EGG_HATCHED = "egg_hatched"

    def __init__(self, name, type):
        """Initializes the monster with its name, type, and starting attributes."""
        self.name = name
        self.type = type
        self.hunger = 100
        self.happiness = 100
        self.stage = "egg"
        self.egg_state = self.EGG_IDLE
        self.age = 0
        self.health = 100
        self.hygiene = 100
        self.base_weight = 50  # Add base weight
        self.weight = self.base_weight  # Initialize current weight to base weight
        self.max_weight = 100  # Add max weight (adjust as needed)
        self.animation_timer = 0
        self.facing_left = False
        self.last_sleep_time = None
        self.consecutive_sleep_days = 0
        self.bounce_height = 0
        self.bounce_speed = 0
        self.bounce_direction = 1  # 1 for moving down, -1 for moving up
        self.x = 580 // 2  # Initial x-coordinate
        self.y = 700 // 2 + 30  # Initial y-coordinate
        self.speed = 15  # Adjust the speed as needed
        self.direction = [
            random.choice([-1, 1]), random.choice([-1, 1])
        ]  # Random initial direction

        # Use a dictionary to store images for different stages/states
        self.images = {
            "egg_idle": pygame.image.load("egg_idle.png"),
            "egg_shake_1_of_2": pygame.image.load("egg_shake_1_of_2.png"),
            "egg_shake_2_of_2": pygame.image.load("egg_shake_2_of_2.png"),
            "egg_hatching": pygame.image.load("egg_hatching.png"),
            "egg_hatched": pygame.image.load("egg_hatched.png"),
            "baby": pygame.image.load("baby_monster.png"),
            "child": pygame.image.load("child_monster.png"),
            "teenager": pygame.image.load("teen_monster.png"),
            "adult": pygame.image.load("adult_monster.png"),
            "special": pygame.image.load("special_monster.png")
        }
        self.image = self.images["egg_idle"]  # Set initial image

        self.image_rect = self.image.get_rect()
        self.image_rect.center = (580 // 2, 700 // 2)
        self.is_sleeping = False
        self.poop_timer = random.randint(600, 1800)
        self.bond = 0
        self.naughtiness = 0
        self.energy = 50
        self.poop_list = []  # Initialize poop_list

        self.evolution = Evolution(self)  # Create an Evolution object for this monster

        # Sickness attributes
        self.is_sick = False
        self.illness = None
        self.sickness_timer = 0  # Add a timer for sickness duration

        # Initialize animations
        self.animations = MonsterAnimations(self)

        # Initialize vomit attributes
        self.vomit_image = None  # Initialize vomit_image
        self.vomit_rect = None  # Initialize vomit_rect

        self.food_image = None
        self.food_rect = None

    def __str__(self):  # Add the __str__ method here
        """Returns a string representation of the Monster object."""
        return (
            f"Monster(name='{self.name}', stage='{self.stage}', "
            f"hunger={self.hunger}, happiness={self.happiness}, "
            f"health={self.health}, hygiene={self.hygiene}, "
            f"age={self.age}, weight={self.weight})")

    def play(self):
        """Plays with the monster, increasing its happiness."""
        self.happiness += 10
        if self.happiness > 100:
            self.happiness = 100

    def clean(self):
        """Cleans the monster, increasing its hygiene."""
        self.hygiene += 15
        if self.hygiene > 100:
            self.hygiene = 100

    def update(self, dt):
        """Updates the monster's state and attributes based on time elapsed."""
        
        # --- Movement (only after hatching) ---
        if self.stage != "egg":  # Check if the monster has hatched
            self._handle_stats_update(dt)  # Update age, hunger, happiness, health

            # --- Sickness logic ---
            self._handle_sickness(dt)

            if self.stage == "egg":
                self.handle_egg_animation()
            else:
                self.handle_monster_animation()

            self.check_evolution()

            # --- Death conditions ---
            if self.health <= 0:
                self.stage = "dead"
                print(f"{self.name} has died! (Health reached 0)")
                return True  # Indicate that the monster has died

            if self.hunger <= 0:
                self.hunger_death_timer -= 1
                if self.hunger_death_timer <= 0:
                    self.stage = "dead"
                    print(f"{self.name} has died! (Starvation)")
                    return True
            else:
                self.hunger_death_timer = 120  # Reset timer if hunger is above 0

                return False  # The monster is still alive

        else:  # If the monster is still an egg
            self.handle_egg_animation()  # Only handle egg animation

        # --- Sleeping logic ---
        if not self.is_sleeping:
            print(f"Monster {self.name} is sleeping. Stats not updated.")
            self.energy += 0.1  
            if self.energy >= 100:
                self.energy = 100
                self.is_sleeping = False
                self.image = self.images[self.stage]  # Use the appropriate image for the current stage
                print(f"Monster {self.name} woke up!")


        # --- Apply bounce effect ---
        if self.bounce_height > 0:
            self.image_rect.y += self.bounce_speed * self.bounce_direction
            self.bounce_height -= abs(self.bounce_speed)  # Decrease remaining bounce height

            if self.bounce_height <= 0:
                self.bounce_direction *= -1  # Change direction
                self.bounce_height = 0  # Stop bouncing when height reaches 0

    def _handle_stats_update(self, dt):
        """Handles updating age, hunger, happiness, and health."""
        # Stage-based aging factor
        if self.stage == "egg":
            aging_factor = 0.01 / 1080  # Divide by 1080
        elif self.stage == "baby":
            aging_factor = 0.05 / 1080  # Divide by 1080
        else:
            aging_factor = 0.02 / 1080  # Divide by 1080

        self.age += aging_factor * dt

        # Hunger and happiness decay
        self.hunger -= 0.1 * dt
        self.happiness -= 0.05 * dt

        # --- Weight-based health decay ---
        if self.weight > self.base_weight:
            weight_penalty = (self.weight - self.base_weight) * 0.01  # Adjust multiplier as needed
            self.health -= weight_penalty * dt

        # Ensure hunger and happiness don't go below 0
        self.hunger = max(0, self.hunger)
        self.happiness = max(0, self.happiness)

        # Health deterioration and regeneration
        self._update_health(dt)

        # Print stat values after updating them
    #       print(f"Hunger: {self.hunger}, Happiness: {self.happiness}, Hygiene: {self.hygiene}, Health: {self.health}")


    def _update_health(self, dt):
        """Calculates and updates health based on happiness, hunger, and hygiene."""
        health_decay = 0
        if self.happiness < 30:
            health_decay += (30 - self.happiness) * 0.01
        if self.hunger < 30:
            health_decay += (30 - self.hunger) * 0.02
        if self.hygiene < 30:
            health_decay += (30 - self.hygiene) * 0.01
        self.health -= health_decay * dt

        # Health regeneration based on high stats
        # If stats are above 70, health increases

        health_increase = 0
        if self.happiness > 70: 
            health_increase += (self.happiness - 70) * 0.01
        if self.hunger > 70: 
            health_increase += (self.hunger - 70) * 0.02
        if self.hygiene > 70: 
            health_increase += (self.hygiene - 70) * 0.01
        self.health += health_increase * dt

        self.health = max(0, min(100, self.health))  # Ensure health stays within 0-100

    def _handle_sickness(self, dt):
        """Handles sickness logic and symptoms."""
        if not self.is_sick:
            sickness_chance = 0 # Probability of getting sick
            if self.happiness < 20:
                sickness_chance += 0.05
            if self.hunger < 20:
                sickness_chance += 0.1
            if self.hygiene < 20:
                sickness_chance += 0.05

            if random.random() < sickness_chance * dt:
                self.is_sick = True
                self.illness = random.choice(["Cold", "Flu", "Tummy Ache"])
                self.sickness_timer = random.randint(120, 300)
                print(f"{self.name} got {self.illness}!")

        if self.is_sick:
            self.sickness_timer -= 1

            if self.illness == "Cold":
                self.happiness -= 0.2 * dt
            elif self.illness == "Flu":
                self.hunger -= 0.1 * dt
            elif self.illness == "Tummy Ache":
                self.happiness -= 0.1 * dt
                self.hunger -= 0.1 * dt

            if self.sickness_timer <= 0:
                self.is_sick = False
                self.illness = None
                print(f"{self.name} recovered from {self.illness}!")


    def handle_egg_animation(self):
        """Handles the egg shaking and hatching animation."""
        self.animation_timer += 1

        if self.animation_timer >= 30:  # Adjust the timing as needed
            self.animation_timer = 0

            if self.egg_state == self.EGG_IDLE:
                self.egg_state = self.EGG_SHAKE_1
                self.image = self.images["egg_shake_1_of_2"]
            elif self.egg_state == self.EGG_SHAKE_1:
                self.egg_state = self.EGG_SHAKE_2
                self.image = self.images["egg_shake_2_of_2"]
            elif self.egg_state == self.EGG_SHAKE_2:
                self.egg_state = self.EGG_HATCHING
                self.image = self.images["egg_hatching"]
            elif self.egg_state == self.EGG_HATCHING:
                shake_amount = 5  # Adjust the shake amount as needed
                self.image_rect.x += random.randint(-shake_amount, shake_amount)
                self.image_rect.y += random.randint(-shake_amount, shake_amount)
                self.egg_state = self.EGG_HATCHED
                self.image = self.images["egg_hatched"]
            elif self.egg_state == self.EGG_HATCHED:
                self.stage = "baby"
                self.image = self.images["baby"]
                
                # --- Set hatching position within the defined box ---
                box_x = 150
                box_y = 370
                box_width = 580 - box_x * 2
                box_height = 700 - box_y - 150 - 110

                self.image_rect.x = random.randint(box_x, box_x + box_width -50 - self.image.get_width())
                self.image_rect.y = random.randint(box_y, box_y + box_height - self.image.get_height())

    def handle_monster_animation(self):
        """Handles monster animations."""
        self.animations.handle_animation()  # Delegate to the MonsterAnimations object

    def check_evolution(self):
        """Calls the check_evolution method of the Evolution object."""
        return self.evolution.check_evolution()  # Delegate to the Evolution object
