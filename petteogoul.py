import pygame
import math

pygame.mixer.init()  # Initialize the mixer

class Petteogoul:
    def __init__(self, screen, image_path, sound_path="petteogoul_sound.wav"):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.show = False
#        self.played_sound = False  # Flag to track if the sound has been played
#        self.sound = pygame.mixer.Sound(sound_path)  # Load the sound effect

        # Arc motion attributes
        self.center_x = screen.get_width() // 2  # X-coordinate of the arc's center
        self.center_y = screen.get_height() // 2  # Y-coordinate of the arc's center
        self.radius = 100  # Radius of the arc
        self.angle = 0  # Current angle in radians
        self.angular_speed = 0.003  # Speed of the angular movement
        
        # Pulse animation attributes
        self.pulse_scale = 1.0       # Current scale of the image
        self.pulse_speed = 0.02     # Speed of the scaling
        self.pulse_direction = 1   # 1 for growing, -1 for shrinking

    def update(self, monster):
        """Checks the monster's health and updates visibility and animation."""
        if monster.health < 95:  # Adjust the threshold as needed
            self.show = True
        else:
            self.show = False

        # Play sound effect when Petteogoul appears
#        if self.show and not self.played_sound:
#            self.sound.play()
#            self.played_sound = True
#        if not self.show:
#            self.played_sound = False

        # Update arc motion (upwards)
        if self.show:
            self.angle += self.angular_speed
            if self.angle > math.pi / 2 or self.angle < -math.pi / 2:  # Reverse direction at the top and bottom of the arc
                self.angular_speed *= -1

            # Update pulsing animation
            self.pulse_scale += self.pulse_speed * self.pulse_direction
            if self.pulse_scale > 1.2 or self.pulse_scale < 0.8:
                self.pulse_direction *= -1  # Change direction


    def draw(self):  # No need to pass monster here
        """Draws the Petteogoul on the screen if visible."""
        if self.show:
            # Calculate position using polar coordinates (for upwards arc)
            x = self.center_x + self.radius * math.sin(self.angle)  # Use sin(angle) for x
            y = self.center_y - self.radius * math.cos(self.angle)  # Use -cos(angle) for y

            # Scale the image for the pulsing effect
            scaled_image = pygame.transform.scale(
                self.image, 
                (int(self.image.get_width() * self.pulse_scale), 
                 int(self.image.get_height() * self.pulse_scale))
            )
            # Center the scaled image at (x, y)
            scaled_rect = scaled_image.get_rect(center=(x, y))
            self.screen.blit(scaled_image, scaled_rect)