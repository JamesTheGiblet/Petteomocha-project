# buttons.py 

import pygame
from monster import Monster

class Button:
    def __init__(self, screen, x, y, width, height, image, label=None, color=(0, 0, 0), highlight_color="yellow"):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.label = label
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, highlighted=False):
        pygame.draw.rect(self.screen, self.color, self.rect, 2, border_radius=10)  # Draw button background
        if highlighted:
            pygame.draw.rect(self.screen, self.highlight_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2, border_radius=10)
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            self.screen.blit(self.image, image_rect)

    def handle_click(self, pos):
        return self.rect.collidepoint(pos)

class Buttons:
    def __init__(self, screen):
        self.screen = screen

        # Button properties
        self.button_diameter = 60
        self.button_radius = self.button_diameter // 2
        self.button_spacing = 20
        self.button_y = self.screen.get_height() - 100 - self.button_diameter + 60

        # Colors
        self.red = (255, 0, 0)

        # Menu button properties
        self.menu_button_width = 55
        self.menu_button_height = 40
        self.menu_button_spacing = 15
        self.top_menu_button_y = 235
        self.bottom_menu_button_y = 475

        # Load button images
        self.top_menu_button_images = {
            "Feed": pygame.transform.scale(pygame.image.load("feed_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6)),
            "Light": pygame.transform.scale(pygame.image.load("light_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6)),
            "Play": pygame.transform.scale(pygame.image.load("play_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6)),
            "Medic": pygame.transform.scale(pygame.image.load("medic_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6))
        }

        self.bottom_menu_button_images = {
            "Clean": pygame.transform.scale(pygame.image.load("cleaning_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6)),
            "Stats": pygame.transform.scale(pygame.image.load("stats_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6)),
            "Shout": pygame.transform.scale(pygame.image.load("shout_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6)),
            "Stroke": pygame.transform.scale(pygame.image.load("stroke_icon.png"), (self.menu_button_width - 6, self.menu_button_height - 6))
        }

        # Create button objects
        self.top_menu_buttons = self.create_menu_buttons(self.top_menu_button_images, self.top_menu_button_y)
        self.bottom_menu_buttons = self.create_menu_buttons(self.bottom_menu_button_images, self.bottom_menu_button_y)

        # Egg images
        self.egg_images = {
            Monster.EGG_IDLE: pygame.image.load("egg_idle.png"),
            Monster.EGG_SHAKE_1: pygame.image.load("egg_shake_1_of_2.png"),
            Monster.EGG_SHAKE_2: pygame.image.load("egg_shake_2_of_2.png"),
            Monster.EGG_HATCHING: pygame.image.load("egg_hatching.png"),
            Monster.EGG_HATCHED: pygame.image.load("egg_hatched.png"),
        }

    def create_menu_buttons(self, images, y_pos):
        buttons = []
        x = (self.screen.get_width() - (4 * self.menu_button_width + 3 * self.menu_button_spacing)) // 2
        for image_name, image in images.items():
            button = Button(self.screen, x, y_pos, self.menu_button_width, self.menu_button_height, image, label=image_name)
            buttons.append(button)
            x += self.menu_button_width + self.menu_button_spacing
        return buttons

    def draw_menu_buttons(self, buttons, highlighted_button=None):
        for button in buttons:
            button.draw(highlighted=button.label == highlighted_button)

    def draw_bottom_red_buttons(self):
        button_x = (self.screen.get_width() - (3 * self.button_diameter + 2 * self.button_spacing)) // 2 - 10
        for i, button_label in enumerate(("A", "B", "C")):
            # Draw the inner (red) circle
            pygame.draw.circle(self.screen, self.red, (button_x + self.button_radius, self.button_y + self.button_radius), self.button_radius - 4)

            # Draw the button label
            font = pygame.font.Font(None, 36)
            text = font.render(button_label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(button_x + self.button_radius, self.button_y + self.button_radius))
            self.screen.blit(text, text_rect)
            button_x += self.button_diameter + self.button_spacing


    def handle_click(self, pos):
        """Handles button clicks."""
        # --- Check bottom red buttons first ---
        button_x = (self.screen.get_width() - (3 * self.button_diameter + 2 * self.button_spacing)) // 2
        for i, button_label in enumerate(("A", "B", "C")):
            button_rect = pygame.Rect(button_x, self.button_y, self.button_diameter, self.button_diameter)
            if button_rect.collidepoint(pos):
                return button_label
            button_x += self.button_diameter + self.button_spacing

        # --- Check menu buttons ---
        for button in self.top_menu_buttons + self.bottom_menu_buttons:
            if button.handle_click(pos):
                return button.label
        return None  # No button clicked
