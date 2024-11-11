# dicspline.py 

def discipline_monster(monster):
    """Disciplines the monster if it has been naughty."""

    if monster.naughtiness > 10:  # Adjust the threshold as needed
        print(f"Disciplining {monster.name}...")

        # Reduce happiness
        monster.happiness -= 10  # Adjust the value as needed
        monster.happiness = max(0, monster.happiness)  # Ensure happiness doesn't go below 0

        # Increase bond
        monster.bond += 5  # Adjust the value as needed
        if monster.bond > 100:
            monster.bond = 100

        print(f"Disciplined! Happiness: {monster.happiness}, Bond: {monster.bond}")

        monster.naughtiness = 0  # Reset naughtiness after discipline

        # Optionally:
        # - Display a discipline animation or image
        # - Play a sound effect

    else:
        print(f"{monster.name} has not been naughty enough to discipline.")
        # Optionally play a sound or show an animation to indicate this
