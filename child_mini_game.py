# child mini game

import pygame


def play_mini_game_child(screen, monster):
    """
    A mini-game for the child stage where the player has to guide the 
    monster through a maze to reach a goal.
    """
    print("Playing child mini-game...")

    # --- Maze generation (simple example) ---
    maze = [
        "#########",
        "#S      #",
        "# # #### #",
        "# #   # #",
        "# ### # #",
        "#   # # #",
        "### # # #",
        "#G   #   #",
        "#########",
    ]
    maze_width = len(maze[0])
    maze_height = len(maze)
    cell_size = 50

    # --- Monster properties ---
    monster_x = 1  # Start position (column)
    monster_y = 1  # Start position (row)
    monster_image = pygame.transform.scale(monster.image, (cell_size, cell_size))

    # --- Goal properties ---
    goal_x = 1  # Goal position (column)
    goal_y = 7  # Goal position (row)
    goal_image = pygame.transform.scale(pygame.image.load("goal.png"), (cell_size, cell_size))  # Load your goal image

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if monster_x > 0 and maze[monster_y][monster_x - 1] != "#":
                        monster_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if monster_x < maze_width - 1 and maze[monster_y][monster_x + 1] != "#":
                        monster_x += 1
                elif event.key == pygame.K_UP:
                    if monster_y > 0 and maze[monster_y - 1][monster_x] != "#":
                        monster_y -= 1
                elif event.key == pygame.K_DOWN:
                    if monster_y < maze_height - 1 and maze[monster_y + 1][monster_x] != "#":
                        monster_y += 1

        # --- Check if reached the goal ---
        if monster_x == goal_x and monster_y == goal_y:
            print("Reached the goal!")
            running = False

        # --- Drawing ---
        screen.fill((255, 255, 255))  # Clear the screen

        # Draw the maze
        for row in range(maze_height):
            for col in range(maze_width):
                if maze[row][col] == "#":
                    pygame.draw.rect(screen, (0, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size))

        # Draw the goal
        screen.blit(goal_image, (goal_x * cell_size, goal_y * cell_size))

        # Draw the monster
        screen.blit(monster_image, (monster_x * cell_size, monster_y * cell_size))

        # Draw the back button
        pygame.draw.rect(screen, back_button_color, back_button_rect)
        font = pygame.font.Font(None, 30)
        text = font.render("Back", True, (255, 255, 255))
        text_rect = text.get_rect(center=back_button_rect.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    print("Exiting child mini-game...")

    # Add to happiness (you can adjust the amount)
    monster.happiness += 20 
    if monster.happiness > 100:
        monster.happiness = 100
    print(f"Mini-game score added to happiness. New happiness: {monster.happiness}")