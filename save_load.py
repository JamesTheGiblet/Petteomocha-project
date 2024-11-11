# save_load.py
import json

def save_game(monster, filename="petteomocha_save.json"):
    """Saves the monster's stats to a JSON file."""
    data = {
        "name": monster.name,
        "stage": monster.stage,
        "hunger": monster.hunger,
        "happiness": monster.happiness,
        "health": monster.health,
        "hygiene": monster.hygiene,
        "age": monster.age,
        "weight": monster.weight,
        # ... add other attributes you want to save ...
    }
    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"Game saved to {filename}")

def load_game(monster, filename="petteomocha_save.json"):
    """Loads the monster's stats from a JSON file."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        monster.name = data["name"]
        monster.stage = data["stage"]
        monster.hunger = data["hunger"]
        monster.happiness = data["happiness"]
        monster.health = data["health"]
        monster.hygiene = data["hygiene"]
        monster.age = data["age"]
        monster.weight = data["weight"]
        # ... load other attributes ...

        # Update the monster's image based on the loaded stage
        monster.image = monster.images[monster.stage]  # Add this line

        print(f"Game loaded from {filename}")
        return True  # Indicate successful loading
    except FileNotFoundError:
        print(f"Save file not found: {filename}")
        return False  # Indicate loading failed