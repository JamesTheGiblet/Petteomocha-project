
# --- Medicine class ---
class Medicine:
    def __init__(self, name, illness_cured, healing_power):
        self.name = name
        self.illness_cured = illness_cured
        self.healing_power = healing_power

# Medicine instances
cold_medicine = Medicine("Cold Medicine", "Cold", 15)
flu_medicine = Medicine("Flu Medicine", "Flu", 20)
tummy_ache_medicine = Medicine("Tummy Ache Medicine", "Tummy Ache", 25)


def heal_monster(monster, medicine=None):  # Add medicine parameter
    """Heals the monster."""

    if monster.is_sick:
        if medicine and medicine.illness_cured == monster.illness:  # Check if the medicine matches the illness
            monster.health += medicine.healing_power  # Use medicine's healing power
            monster.health = min(100, monster.health)
            monster.is_sick = False
            monster.illness = None
            print(f"Cured {monster.name} of {medicine.illness_cured}! Health: {monster.health}")
        else:
            print(f"That medicine doesn't work for {monster.illness}!")
    else:
        if medicine:
            print(f"{monster.name} is not sick, no need for {medicine.name}!")
        else:
            print(f"{monster.name} is not sick!")

        # Optionally play a sound or show an animation to indicate no sickness