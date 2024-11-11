import pygame
import random

class Backgrounds:
    def __init__(self, screen):
        self.screen = screen

        # Load background images with variations
        self.backgrounds = {
            "day_sunny": pygame.transform.scale(pygame.image.load("day_background.png"), (300, 300)),
            "night_clear": pygame.transform.scale(pygame.image.load("night_background.png"), (300, 300)),
            "day_rainy": pygame.transform.scale(pygame.image.load("day_rainy.png"), (300, 300)),  # Example rainy background
            "day_snowy": pygame.transform.scale(pygame.image.load("day_snowy.png"), (300, 300)),  # Example snowy background
            # ... add more backgrounds for different seasons/events ...
        }

        # Load sun and moon images
        self.sun_image = pygame.image.load("sun.png")  
        self.moon_image = pygame.image.load("moon.png")

        # Load and scale cloud images with depth/layer information
        self.clouds = [
            {"image": pygame.transform.scale(pygame.image.load("large_cloud.png"), (100, 60)), "x": random.randint(100, 375), "y": random.randint(220, 260), "speed": random.uniform(0.2, 0.4), "direction": random.choice([-1, 1]), "depth": 0.2},  # Further back
            {"image": pygame.transform.scale(pygame.image.load("medium_cloud.png"), (80, 50)), "x": random.randint(100, 375), "y": random.randint(220, 260), "speed": random.uniform(0.4, 0.8), "direction": random.choice([-1, 1]), "depth": 0.5},  # Mid-ground
            {"image": pygame.transform.scale(pygame.image.load("small_cloud.png"), (60, 40)), "x": random.randint(100, 375), "y": random.randint(220, 260), "speed": random.uniform(0.6, 0.9), "direction": random.choice([-1, 1]), "depth": 0.8}   # Closer
        ]

        self.current_background = self.backgrounds["day_sunny"]  # Start with day background

        # Sun/moon animation variables
        self.sun_moon_x = 135 + 10  # Initial x-coordinate for sun/moon
        self.sun_moon_y = 225 + 10  # Initial y-coordinate for sun/moon
        self.sun_moon_speed = 0.1  # Adjust the speed as needed
        self.day_fraction = 0  # Initialize day_fraction

    def update(self, monster_age):
        """Updates the current background and animates the clouds."""

        # --- Background selection logic ---
        self.day_fraction = monster_age % 1  # Update day_fraction

        if 0 <= self.day_fraction <= 0.5:  # Daytime
            # Example: Randomly choose between sunny and rainy during the day
            if random.random() < 0.8:  # 80% chance of sunny
                self.current_background = self.backgrounds["day_sunny"]
            else:
                self.current_background = self.backgrounds["day_rainy"]
        else:  # Nighttime
            self.current_background = self.backgrounds["night_clear"]

        # --- Cloud animation with parallax scrolling ---
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"] * cloud["direction"] * cloud["depth"]  # Multiply speed by depth
            if cloud["x"] > 375 or cloud["x"] < 100:  
                cloud["direction"] *= -1

        # --- Sun/Moon animation ---
        self.sun_moon_x = 135 + int((self.day_fraction * 300)) - 50  # Update sun/moon x-coordinate


    def draw(self):
        """Draws the current background, sun/moon, and clouds on the screen."""
        self.screen.blit(self.current_background, (135, 225))

        # Draw clouds (grayscale if it's nighttime)
        for cloud in self.clouds:
            if self.current_background == self.backgrounds["night_clear"]:  # Check against the night background key
                cloud_image = cloud["image"].copy()
                cloud_image.set_colorkey((0, 0, 0))  # Assuming black is the background color
                gray_cloud = pygame.transform.grayscale(cloud_image)
                self.screen.blit(gray_cloud, (cloud["x"], cloud["y"]))
            else:
                self.screen.blit(cloud["image"], (cloud["x"], cloud["y"]))

        # Draw sun or moon (based on day_fraction)
        if 0 <= self.day_fraction <= 0.5:  # If it's daytime
            self.screen.blit(self.sun_image, (self.sun_moon_x, self.sun_moon_y))
        else:  # If it's nighttime
            self.screen.blit(self.moon_image, (self.sun_moon_x, self.sun_moon_y))
