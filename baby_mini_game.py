# baby mini game

import random
import pygame


def play_mini_game_baby(screen, monster):
    """
    A simple mini-game for the baby stage where the player has to click 
    on the monster as it moves around the screen.
    """
    print("Playing baby mini-game...")

    monster_image = monster.image  # Use the monster's current image
    monster_x = random.randint(0, screen.get_width() - monster_image.get_width())
    monster_y = random.randint(0, screen.get_height() - monster_image.get_height())
    monster_speed = 1

    score = 0
    font = pygame.font.Font(None, 36)

    # Back button properties
    back_button_rect = pygame.Rect(10, 10, 80, 40)
    back_button_color = (255, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    print("Back button clicked")
                    running = False
                else:
                    # Check if the click collides with the monster
                    monster_rect = pygame.Rect(monster_x, monster_y, monster_image.get_width(), monster_image.get_height())
                    if monster_rect.collidepoint(event.pos):
                        score += 1
                        monster_x = random.randint(0, screen.get_width() - monster_image.get_width())
                        monster_y = random.randint(0, screen.get_height() - monster_image.get_height())
                        monster_speed += 0.2  # Increase speed slightly

        # --- Monster movement ---
        monster_x += random.choice([-monster_speed, monster_speed])
        monster_y += random.choice([-monster_speed, monster_speed])

        # --- Keep monster within bounds ---
        monster_x = max(0, monster_x)
        monster_x = min(screen.get_width() - monster_image.get_width(), monster_x)
        monster_y = max(0, monster_y)
        monster_y = min(screen.get_height() - monster_image.get_height(), monster_y)

        # --- Drawing ---
        screen.fill((255, 255, 255))  # Clear the screen

        # Draw the monster
        screen.blit(monster_image, (monster_x, monster_y))

        # Draw the score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, screen.get_height() - 50))

        # Draw the back button
        pygame.draw.rect(screen, back_button_color, back_button_rect)
        font = pygame.font.Font(None, 30)
        text = font.render("Back", True, (255, 255, 255))
        text_rect = text.get_rect(center=back_button_rect.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    print("Exiting baby mini-game...")

    # Add the score to the monster's happiness
    monster.happiness += score  # You can adjust the multiplier as needed
    if monster.happiness > 100:
        monster.happiness = 100
    print(f"Mini-game score added to happiness. New happiness: {monster.happiness}")