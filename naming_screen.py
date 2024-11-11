import pygame
from monster import Monster

def handle_naming_screen(screen, background_image):
    """Handles the naming screen where the player enters the monster's name."""

    print("Entering naming screen...")

    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(185, 300, 140, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    black = (0, 0, 0)
    red = (255, 0, 0)  # For error message
    done = False
    cursor_visible = True
    cursor_blink_rate = 500  # in milliseconds
    cursor_last_blink = pygame.time.get_ticks()

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                print("Exiting naming screen (window closed)...")
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text:  # Check if a name has been entered
                            monster = Monster(text, "Egg")
                            done = True
                            print(f"Name entered: {text}")
                        else:
                            print("Please enter a name.")  # Handle empty name input
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Drawing
        screen.fill((255, 255, 255))  # Clear the screen
        screen.blit(background_image, (140, 225))  # Blit the background image

        # Render and blit the question text
        question_surface = font.render("Name your Petteomocha:", True, black)
        question_rect = question_surface.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(question_surface, question_rect)

        # Render and blit the text surface with cursor
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Draw blinking cursor
        if active and cursor_visible:
            cursor_pos = (input_box.x + 5 + txt_surface.get_width(), input_box.y + 10)
            pygame.draw.line(screen, color, cursor_pos, (cursor_pos[0], cursor_pos[1] + 30), 2)

        # Blink the cursor
        now = pygame.time.get_ticks()
        if now - cursor_last_blink > cursor_blink_rate:
            cursor_last_blink = now
            cursor_visible = not cursor_visible

        # Draw the input box rectangle with thicker border when active
        border_width = 4 if active else 2
        pygame.draw.rect(screen, color, input_box, border_width)

        # Display error message for empty input
        if not text and not active:
            error_text = font.render("Please enter a name.", True, red)
            error_rect = error_text.get_rect(center=(screen.get_width() // 2, 370))
            screen.blit(error_text, error_rect)

        pygame.display.flip()

    print(f"Exiting naming screen, created monster: {monster.name}")
    return monster