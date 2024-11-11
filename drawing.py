# drawing.py 

from game_state import GameState

def draw_monster(screen, monster, buttons):
    """Draws the monster, including any active animation frames, poop, vomit, and food."""
    screen.get_rect()

    if monster.stage == "egg":
        image = buttons.egg_images[monster.egg_state]
    else:
        # Corrected line: Access the animations dictionary from the MonsterAnimations object
        animation_frames = monster.animations.animations.get(monster.current_animation, [monster.image])  
        image = animation_frames[int(monster.animation_frame)]

    image_rect = image.get_rect()
    image_rect.center = (monster.x, monster.y)  # Use monster.x and monster.y for positioning
    image_rect.x -= 0
    image_rect.y += 85
    screen.blit(image, image_rect)
    monster.image_rect = image_rect

    for poop in monster.poop_list:
        screen.blit(poop["image"], poop["rect"])

    if monster.vomit_image:
        screen.blit(monster.vomit_image, monster.vomit_rect)

    if monster.food_image:
        screen.blit(monster.food_image, monster.food_rect)

def draw_menus(screen, buttons, menu_state, selected_button):
    """Draws the menus with the selected button highlighted."""

    if menu_state != GameState.NO_MENU:
        buttons.draw_menu_buttons(buttons.top_menu_buttons, highlighted_button=selected_button)
        buttons.draw_menu_buttons(buttons.bottom_menu_buttons, highlighted_button=selected_button)

def draw_game(screen, background_image, egg_case_image, monster, buttons, menu_state, selected_button):
    """Draws the entire game scene, including background, monster, and menus."""

    screen.blit(background_image, (135, 225))
    screen.blit(egg_case_image, (0, 0))

    draw_monster(screen, monster, buttons)

    draw_menus(screen, buttons, menu_state, selected_button)

    buttons.draw_bottom_red_buttons()
