import pygame
import random

def play_mini_game(screen, monster):
    """
    Plays a mini-game where the player (happy.png) has to catch falling food.
    Adds the score to the monster's happiness when the mini-game is exited.
    """
    print("Starting mini-game...")

    # --- Game variables ---
    player_image = pygame.image.load("happy.png")  # Load happy.png for the player
    player_width = player_image.get_width()
    player_height = player_image.get_height()
    player_x = screen.get_width() // 2 - player_width // 2
    player_y = screen.get_height() - 100 - player_height
    player_speed = 1

    # Load food images (you'll need to have these images)
    food_images = {
        "apple": pygame.image.load("apple.png"),
        "cake": pygame.image.load("cake.png"),
        # ... add more food images
    }
    current_food = random.choice(list(food_images.keys()))  # Choose a random food to start
    object_image = food_images[current_food]
    object_width = object_image.get_width()
    object_height = object_image.get_height()
    object_x = random.randint(0, screen.get_width() - object_width)
    object_y = -object_height  # Start off-screen
    object_speed = 2

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

        # --- Handle continuous movement when keys are held down ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # --- Keep player within bounds ---
        player_x = max(0, player_x)
        player_x = min(screen.get_width() - player_width, player_x)

        # --- Object movement ---
        object_y += object_speed
        if object_y > screen.get_height():
            current_food = random.choice(list(food_images.keys()))
            object_image = food_images[current_food]
            object_width = object_image.get_width()
            object_height = object_image.get_height()
            object_x = random.randint(0, screen.get_width() - object_width)
            object_y = -object_height

        # --- Collision detection ---
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        object_rect = pygame.Rect(object_x, object_y, object_width, object_height)
        if player_rect.colliderect(object_rect):
            score += 1
            current_food = random.choice(list(food_images.keys()))
            object_image = food_images[current_food]
            object_width = object_image.get_width()
            object_height = object_image.get_height()
            object_x = random.randint(0, screen.get_width() - object_width)
            object_y = -object_height

        # --- Drawing ---
        screen.fill((255, 255, 255))  # Clear the screen

        # Draw the player (happy.png)
        screen.blit(player_image, (player_x, player_y))

        # Draw the falling food
        screen.blit(object_image, (object_x, object_y))

        # Draw the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, screen.get_height() - 50))

        # Draw the back button
        pygame.draw.rect(screen, back_button_color, back_button_rect)
        font = pygame.font.Font(None, 30)
        text = font.render("Back", True, (255, 255, 255))
        text_rect = text.get_rect(center=back_button_rect.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    print("Exiting mini-game...")

    # Add the score to the monster's happiness
    monster.happiness += score  # You can adjust the multiplier as needed
    if monster.happiness > 100:
        monster.happiness = 100
    print(f"Mini-game score added to happiness. New happiness: {monster.happiness}")
