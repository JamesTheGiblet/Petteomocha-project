from baby_mini_game import play_mini_game_baby
from child_mini_game import play_mini_game_child
from game_logic import decrease_weight
from game_state import GameState
from feeding import feed_monster, display_food, apple, cake, steak, burger  # Import food instances
from sleeping import put_monster_to_sleep
from mini_game import play_mini_game  # You'll need to create this module
from healing import heal_monster, cold_medicine, flu_medicine, tummy_ache_medicine  # Import medicine instances
from discipline import discipline_monster
from stroke import stroke_monster
from stats_display import show_stats
from cleaning import clean_up_poop
import random
from teen_mini_game import play_mini_game_teenager


def handle_button_navigation(clicked_button, menu_state, selected_button, monster, screen, background_image, egg_case_image, buttons):
    """Handles button navigation and actions within menus."""

    print(f"Button Navigation: clicked_button={clicked_button}, menu_state={menu_state}, selected_button={selected_button}")

    if clicked_button == "A":
        button_labels = ("Feed", "Light", "Play", "Medic", "Clean", "Stats", "Shout", "Stroke")
        try:
            current_index = button_labels.index(selected_button)
            selected_button = button_labels[(current_index + 1) % len(button_labels)]
        except ValueError:
            print(f"Error: Button '{selected_button}' not found in button_labels")
            selected_button = "Feed"

    elif clicked_button == "C":
        menu_state = GameState.TOP_MENU if menu_state == GameState.NO_MENU else GameState.NO_MENU
        selected_button = "Feed" if menu_state == GameState.TOP_MENU else None

    elif clicked_button == "B":
        if selected_button == "Feed":

            print("Button B pressed, feeding monster...")

            food_choices = [apple, cake, steak, burger]
            food_to_feed = random.choice(food_choices)

            display_food(monster)  # Display the food before feeding
            feed_monster(monster, food_to_feed)  # Pass the selected food to feed_monster

        elif selected_button == "Light":

            print("Button B pressed, putting monster to sleep...")
            put_monster_to_sleep(monster)

        elif selected_button == "Play":

            print("Button B pressed, starting mini-game...")

            # --- Game selection based on monster stage ---
            if monster.stage == "baby":
                play_mini_game_baby(screen, monster)  # Example: Simple game for baby stage
            elif monster.stage == "child":
                play_mini_game_child(screen, monster)  # Example: Slightly more complex game for child stage
            elif monster.stage == "teenager":
                play_mini_game_teenager(screen, monster)  # Example: More challenging game for teenager stage
            else:
                play_mini_game(screen, monster)  # Default game for other stages

            decrease_weight(monster)  # Decrease weight after playing

        elif selected_button == "Medic":

            print("Button B pressed, healing monster...")
            # --- Medicine selection ---
            if monster.is_sick:
                # Determine available medicines based on the monster's illness
                available_medicines = {
                    "Cold": cold_medicine,
                    "Flu": flu_medicine,
                    "Tummy Ache": tummy_ache_medicine,
                }
                selected_medicine = available_medicines.get(monster.illness)
                if selected_medicine:
                    heal_monster(monster, selected_medicine)  # Pass the selected medicine
                else:
                    print(f"No medicine available for {monster.illness}!")
            else:
                print(f"{monster.name} is not sick!")

        elif selected_button == "Clean":

            print("Button B pressed, cleaning up poop...")
            clean_up_poop(monster)

        elif selected_button == "Stats":

            print("Button B pressed, showing stats...")
            show_stats(screen, monster, background_image, egg_case_image, buttons)

        elif selected_button == "Shout":

            print("Button B pressed, disciplining monster...")
            discipline_monster(monster)

        elif selected_button == "Stroke":

            print("Button B pressed, stroking monster...")
            stroke_monster(monster)

    print(f"Button Navigation: returning selected_button={selected_button}, menu_state={menu_state}")

    return selected_button, menu_state
