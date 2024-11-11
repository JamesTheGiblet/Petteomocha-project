# game_state.py 

import pygame
from enum import Enum  # Import Enum

class GameState(Enum):  # Define GameState as an Enum
    NAMING = 0
    MAIN_GAME = 1
    PAUSED = 2
    NO_MENU = 3  # No menu displayed
    TOP_MENU = 4  # Top menu displayed
    BOTTOM_MENU = 5  # Bottom menu displayed 
    DEAD = 6  # New state for when the monster is dead
    END = 7  # Add this line to define the END state

def handle_game_state(current_state, events):
    """Handles changes in the game state based on events."""

    new_state = current_state  # Initialize new_state with the current state

    if current_state == GameState.NAMING:
        # Handle naming input and transition to MAIN_GAME
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    new_state = GameState.MAIN_GAME  # Update new_state
                    print("Transitioning to MAIN_GAME state")  

    elif current_state == GameState.MAIN_GAME:
        # Handle main game events and logic (this will be handled in petteomocha.py)
        pass  

    elif current_state == GameState.PAUSED:
        # Handle pause menu events and logic
        pass

    return new_state  # Return the new game state