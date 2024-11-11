# cleaning.py

def clean_up_poop(monster):
    """
    Cleans up the monster's poop or vomit, adjusting happiness and hygiene accordingly.
    Removes the poop/vomit images and resets the relevant attributes.
    """
    print(f"Cleaning up after {monster.name}...")

    had_poop = len(monster.poop_list) > 0
    had_vomit = monster.vomit_image is not None  # Check if there was vomit

    # Remove all poop and vomit images
    monster.poop_list = []
    monster.vomit_image = None

    # Adjust happiness and hygiene (different values for poop and vomit)
    if had_poop:
        monster.happiness += 10  # Increase for cleaning poop
        monster.hygiene += 15  # Increase for cleaning poop
    if had_vomit:
        monster.happiness += 5   # Increase for cleaning vomit (less than poop)
        monster.hygiene += 20  # Increase more for cleaning vomit

    # Ensure stats don't go below 0
    monster.happiness = max(0, monster.happiness)
    monster.hygiene = max(0, monster.hygiene)

    # Cap happiness and hygiene at 100
    monster.happiness = min(100, monster.happiness)
    monster.hygiene = min(100, monster.hygiene)

    print(f"Cleaned up! Happiness: {monster.happiness}, Hygiene: {monster.hygiene}")