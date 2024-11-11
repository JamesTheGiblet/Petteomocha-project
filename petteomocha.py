# petteomocha.py 

import pygame
from monster import Monster
from buttons import Buttons
from game_state import GameState, handle_game_state
from game_logic import update_monster, handle_button_click
from drawing import draw_monster, draw_menus
from naming_screen import handle_naming_screen
from menu_navigation import handle_button_navigation
from stats_display import show_stats
from petteogoul import Petteogoul
from backgrounds import Backgrounds
from death_screen import handle_death_screen
from save_load import save_game, load_game  # Import from save_load.py


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((580, 700))

        # Initialize backgrounds
        self.backgrounds = Backgrounds(self.screen)
        self.egg_case_image = pygame.image.load("egg_case.png")
        self.tombstone_image = pygame.image.load(
            "tomb_stone1.png")  # Load the tombstone image
        self.buttons = Buttons(self.screen)
        self.monster = Monster("DefaultName", "Egg")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.game_state = GameState.NAMING
        self.menu_state = GameState.NO_MENU
        self.selected_button = None
        self.food_items = {}
        self.show_evolution_message = False
        self.evolution_message_timer = 0
        self.petteogoul = Petteogoul(self.screen, "petteogoul.png")

        # Initialize game results dictionary
        self.game_results = {
            "times_fed": 0,
            "times_played": 0,
            "best_stat": "",
            "worst_stat": "",
            "evo_stat": ""
        }

    def run(self):
        """Runs the main game loop."""
        running = True

        # --- Load game at start ---
        if load_game(self.monster):  # Try to load the game
            self.game_state = GameState.MAIN_GAME  # Start in the main game if loaded successfully

        while running:
            events = pygame.event.get()
            self.game_state = handle_game_state(self.game_state, events)

            if self.game_state == GameState.NAMING:
                self.handle_naming_screen()

                # Print the monster's state after naming
                print(self.monster)  # This line prints the monster's info

            elif self.game_state == GameState.MAIN_GAME:
                self.handle_main_game(events)
            elif self.game_state == GameState.DEAD:  # Handle the DEAD state
                if handle_death_screen(self.screen, self.tombstone_image,
                                    self.monster, self.buttons,
                                    self.backgrounds.current_background,
                                    self.egg_case_image, self.menu_state,
                                    self.selected_button, self.game_results
                                    ):  # Call the imported function
                    # Reset the game state if "Play Again" is clicked
                    self.game_state = GameState.NAMING
                    self.monster = Monster("DefaultName",
                                        "Egg")  # Create a new monster
                else:
                    running = False  # Quit the game if "Quit" is clicked

            pygame.display.flip()

        pygame.quit()

    def handle_naming_screen(self):
        self.monster = handle_naming_screen(
            self.screen, self.backgrounds.backgrounds["day_sunny"]
        )  # Updated line
        self.game_state = GameState.MAIN_GAME
        self.menu_state = GameState.NO_MENU
        self.selected_button = None

    def handle_main_game(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                save_game(self.monster)  # Save on exit
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse click:", event.pos)  # Add this line to print mouse click position
                self.handle_mouse_click(event)

            if event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_ESCAPE:  # If Esc key is pressed
                    print("Exiting game...")
                    save_game(self.monster)  # Save the game before exiting
                    pygame.quit()
                    exit()

        # --- Drawing ---
        self.draw_game()  # Call the draw_game method to handle drawing

        # --- Update Game Logic ---  (Moved this block after drawing)
        dt = self.clock.tick(self.FPS) / 1000  # Get delta time
        update_monster(self.monster, dt, self.screen)  # Pass self.screen to the function

        # --- Check if the monster has died ---
        if self.monster.update(dt):
            self.game_state = GameState.DEAD

        # --- Check for evolution ---
        if self.monster.check_evolution():
            self.show_evolution_message = True
            self.evolution_message_timer = 5

        # --- Display evolution message ---
        if self.show_evolution_message:
            self.display_evolution_message()
            self.evolution_message_timer -= dt
            if self.evolution_message_timer <= 0:
                self.show_evolution_message = False

        # --- Update animation ---
        if self.monster.current_animation:
            self.monster.animation_frame += self.monster.animation_speed * dt
            if self.monster.animation_frame >= len(
                    self.monster.animations.animations
                    [self.monster.current_animation]):
                self.monster.animation_frame = 0
                if self.monster.current_animation in ("eating", "sleeping"):
                    self.monster.current_animation = None

        # --- Update Petteogoul ---
        self.petteogoul.update(self.monster)

        # --- Update and Draw Background ---
        self.backgrounds.update(
            self.monster.age)  # Pass the monster's age to update()

        # --- Drawing ---
        self.draw_game()  # Call the draw_game method to handle drawing

    def handle_mouse_click(self, event):
        clicked_button = self.buttons.handle_click(event.pos)
        if clicked_button:
            if clicked_button in ("A", "B", "C"):  # Red button clicks
                self.selected_button, self.menu_state = handle_button_navigation(
                    clicked_button, self.menu_state, self.selected_button, self.monster, self.screen,
                    self.backgrounds.current_background, self.egg_case_image, self.buttons
                )

            else:  # Menu button clicks
                if clicked_button == "Stats":
                    self.show_stats()  # Show stats screen
                elif clicked_button == "Feed":
                    selected_food = self.food_items.get(self.selected_button)
                    if selected_food:
                        handle_button_click(self.monster, clicked_button)
                    else:
                        handle_button_click(self.monster, clicked_button)

    def show_stats(self):
        show_stats(self.screen, self.monster, self.backgrounds.current_background, self.egg_case_image, self.buttons)

    def display_evolution_message(self):
        """Displays a message on the screen about the special evolution."""
        font = pygame.font.Font(None, 48)  # Choose a font size
        message_text = font.render("ZEN MASTER EVOLUTION!", True, (255, 255, 0))  # Yellow text
        message_rect = message_text.get_rect(center=(self.screen.get_width() // 2, 100))  # Position at the top
        self.screen.blit(message_text, message_rect)

    def draw_game(self):  
        """Draws the entire game scene."""

        self.backgrounds.draw()  # Draw the background and clouds FIRST

        self.screen.blit(self.egg_case_image, (0, 0))  # Draw the egg case

        draw_monster(self.screen, self.monster, self.buttons)  # Call draw_monster to draw the monster, poop, and vomit
        
        self.petteogoul.draw()  # Draw the Petteogoul if visible

#        self.monster.draw_thought_bubble(self.screen)  # Call draw_thought_bubble on the monster

        draw_menus(self.screen, self.buttons, self.menu_state, self.selected_button)

        self.buttons.draw_bottom_red_buttons()

if __name__ == "__main__":
    game = Game()
    game.run()

