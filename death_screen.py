import pygame
from drawing import draw_game  # Import your draw_game function

def handle_death_screen(screen, tombstone_image, monster, buttons, background_image, egg_case_image, menu_state, selected_button, game_results):
    """Displays the death screen with the tombstone and game results."""
    # Replace the monster's image with the tombstone
    monster.image = tombstone_image
    monster.image_rect = monster.image.get_rect(center=(screen.get_width() // 2, monster.image_rect.centery))

    # Draw the game scene with the tombstone (call your draw_game function)
    draw_game(screen, background_image, egg_case_image, monster, buttons, menu_state, selected_button)  

    pygame.display.flip()

    # Display game results
    display_game_results(screen, game_results)

    # Add "Play Again" and "Quit" buttons
#    play_again_button = pygame.Rect(100, 400, 150, 50)  # Adjust position and size as needed
#    quit_button = pygame.Rect(330, 400, 150, 50)  # Adjust position and size as needed

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  
    # Check for mouse clicks
                clicked_button = buttons.handle_click(event.pos)  # Use your buttons.handle_click()
                if clicked_button == "A":  # A button
                    print("Play Again button clicked")
                    return True  # Indicate play again
                elif clicked_button == "B":  # B button
                    print("Quit button clicked")
                    return False  # Indicate quit

        # Draw the buttons
#        pygame.draw.rect(screen, (0, 255, 0), play_again_button)  # Green for play again
#        pygame.draw.rect(screen, (255, 0, 0), quit_button)  # Red for quit

        # Add button text (you can customize this)
#        font = pygame.font.Font(None, 36)
#        play_text = font.render("Play Again", True, (0, 0, 0))
#        play_text_rect = play_text.get_rect(center=play_again_button.center)
#        screen.blit(play_text, play_text_rect)

#        quit_text = font.render("Quit", True, (0, 0, 0))
#        quit_text_rect = quit_text.get_rect(center=quit_button.center)
#        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

def display_game_results(screen, game_results):
    """Displays the game results."""
    # ... (your existing code to display results) ...
    font = pygame.font.Font(None, 36)

    # ... (Calculate and display the results here) ...
    # Example (replace with your actual results data and display logic):
    times_fed = game_results["times_fed"]
    times_played = game_results["times_played"]
    best_stat = game_results["best_stat"]
    worst_stat = game_results["worst_stat"]
    evo_stat = game_results["evo_stat"]
    
    results_text = [
        "Game Over",
        f"Times Fed: {times_fed}",
        f"Times Played: {times_played}",
        f"Best Stat: {best_stat}",
        f"Worst Stat: {worst_stat}",
        f"Evo' Stat: {evo_stat}"
    ]

    y_pos = 270
    for i, line in enumerate(results_text):
        if i == 0:
            text_surface = font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y_pos))
            screen.blit(text_surface, text_rect)
            pygame.draw.line(screen, (255, 0, 0), (text_rect.left, text_rect.bottom + 5), (text_rect.right, text_rect.bottom + 5), 2)
        else:
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(150, y_pos))
            screen.blit(text_surface, text_rect)
        y_pos += 40

    pygame.display.flip()