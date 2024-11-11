import pygame

class MonsterAnimations:
    def __init__(self, monster):
        self.monster = monster
        self.animations = {
            "eating": [
                pygame.image.load("baby_eating1.png"),
                pygame.image.load("baby_eating2.png"),
                pygame.image.load("baby_eating3.png")
                # Add more frames as needed
            ],
            "sleeping": [
                pygame.image.load("baby_sleeping1.png"),
                pygame.image.load("baby_sleeping2.png"),
                pygame.image.load("baby_sleeping3.png")
                # Add more frames as needed
            ],
            # You can add more animation sequences here...
        }
        self.monster.current_animation = None
        self.monster.animation_frame = 0
        self.monster.animation_speed = 0.1  # Adjust as needed

    def handle_animation(self):
        """Handles animations for the monster."""
        if self.monster.current_animation:
            self.monster.animation_frame += self.monster.animation_speed
            if self.monster.animation_frame >= len(self.animations[self.monster.current_animation]):
                self.monster.animation_frame = 0
                if self.monster.current_animation in ("eating", "sleeping", "stroking"):  # Include "stroking" here
                    self.monster.current_animation = None
                    self.monster.image = self.monster.images[self.monster.stage]  # Reset to default image