# evolution.py 

import random
import monster

class Evolution:
    def __init__(self, monster):
        self.monster = monster

    def check_evolution(self):
        """Checks if the monster should evolve to the next stage."""

        # --- Regular Evolutions ---
        if self.monster.stage == "egg" and self.monster.hunger < 50:
            self.evolve_to("baby")
        elif self.monster.stage == "baby" and self.monster.age >= 1 and self.monster.bond >= 60:
            self.evolve_to("child")
        elif (self.monster.stage == "child" and 
                self.monster.age >= 3 and 
                self.monster.happiness > 80 and 
                self.monster.naughtiness >= 20):  # Discipline condition
                self.evolve_to("teenager")
        elif (self.monster.stage == "teenager" and 
                self.monster.age >= 5 and 
                self.monster.health > 90 and
                50 <= self.monster.weight <= 70):  # Weight condition
            self.evolve_to("adult")

        # --- Special Evolutions ---


        # Zen Master Evolution
        if (self.monster.stage == "adult" and 
            self.monster.hunger >= 50 and 
            self.monster.consecutive_sleep_days >= 7 and 
            self.monster.bond >= 80):
            self.evolve_to("special")
            print("ZEN MASTER EVOLUTION ACHIEVED!")
            return True

        # Petteshibo evolution (example)
        if self.monster.stage == "adult" and self.monster.weight >= 80:  # Access monster attributes using self.monster
            self.evolve_to("petteshibo")  # Assuming you have "petteshibo" in monster.images
            print("PETTESHIBO EVOLUTION ACHIEVED!")
            return True

        return False

    def evolve_to(self, new_stage):
        """Evolves the monster to the specified stage."""

        self.monster.stage = new_stage
        self.monster.image = self.monster.images[new_stage]

        # Stage-specific attribute adjustments
        if new_stage == "baby":
            self.monster.hunger = 80
            self.monster.happiness = 60  # Lower initial happiness
            self.monster.poop_timer = random.randint(100, 300)  # Poops more frequently
        elif new_stage == "child":
            self.monster.happiness = 90
            self.monster.energy = 80  # More energy
            self.monster.naughtiness = 30  # Slightly naughty
        elif new_stage == "teenager":
            self.monster.energy = 40  # Needs more sleep
            self.monster.naughtiness = 60  # More naughty
        elif new_stage == "adult":
            self.monster.health = 100  # Full health in adult stage
            self.monster.hygiene = 90  # Good hygiene 
        elif new_stage == "special":
            self.monster.hunger = 100
            self.monster.happiness = 100
            self.monster.health = 100
            self.monster.hygiene = 100
            self.monster.energy = 100

                # Petteshibo evolution (example)
        if self.monster.stage == "adult" and monster.weight >= 80:  # Adjust threshold as needed
            self.evolve_to("petteshibo")  # Assuming you have "petteshibo" in monster.images
            print("PETTESHIBO EVOLUTION ACHIEVED!")
            return True

        # ... add more adjustments for other stages as needed ...