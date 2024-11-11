import pygame

from drawing import draw_monster

def show_stats(screen, monster, background_image, egg_case_image, buttons):
    """Displays a new surface with the monster's stats, using icons and progress bars."""
    print("Showing monster stats...")

    # --- Scale down the stats surface ---
    stats_surface_width = 300
    stats_surface_height = 350  # Reduced size
    stats_surface = pygame.Surface((stats_surface_width, stats_surface_height))
    stats_surface.fill((255, 255, 255))
    font = pygame.font.Font(None, 24)
    text_color = (0, 0, 0)

    stats_data = {
        "Name": (monster.name, None, None),  # No bar or special color for Name
        "Age": (monster.age, (0, 128, 0), None),  # Green bar
        "Hunger": (monster.hunger, (255, 0, 0), 30),  # Red bar if below 30
        "Happiness": (monster.happiness, (255, 0, 0), 30),  # Red bar if below 30
        "Hygiene": (monster.hygiene, (0, 128, 0), None),  # Green bar
        "Energy": (monster.energy, (0, 128, 0), None),  # Green bar
        "Bond": (monster.bond, (0, 128, 0), None),  # Green bar
        "Health": (monster.health, (255, 0, 0), 30),  # Red bar if below 30
        "Weight": (monster.weight, (0, 0, 255), None),  # Blue bar for weight
    }

    # --- Calculate total height needed for all stats ---
    icon_height = 32
    text_height = font.get_height()
    bar_height = 15
    spacing = 10
    total_stats_height = len(stats_data) * (icon_height + text_height + bar_height + spacing) + spacing  # Add spacing between stats

    # --- Create a scrollable surface ---
    scrollable_surface = pygame.Surface((stats_surface_width, total_stats_height)) 
    scrollable_surface.fill((255, 255, 255))

    # --- Draw stats on the scrollable surface ---
    icon_x = 20
    bar_x = 150
    bar_width = 100
    y_coord = spacing  # Start with spacing at the top

    icons = {
        "Name": pygame.image.load("name_icon.png"),
        "Age": pygame.image.load("age_icon.png"),
        "Hunger": pygame.image.load("hunger_icon.png"),
        "Happiness": pygame.image.load("happiness_icon.png"),
        "Hygiene": pygame.image.load("hygiene_icon.png"),
        "Energy": pygame.image.load("energy_icon.png"),
        "Bond": pygame.image.load("bond_icon.png"),
        "Health": pygame.image.load("health_icon.png"),
        "Weight": pygame.image.load("weight_icon.png"),  # Make sure you have this icon
    }

    for stat_name, (stat_value, bar_color, threshold) in stats_data.items():
        icon = pygame.transform.scale(icons[stat_name], (32, 32))
        scrollable_surface.blit(icon, (icon_x, y_coord))

        # Draw stat name and value (formatted to 1 decimal place if it's a number)
        if isinstance(stat_value, (int, float)):  # Check if stat_value is a number
            stat_text = font.render(f"{stat_name}: {stat_value:.1f}", True, text_color)
        else:
            stat_text = font.render(f"{stat_name}: {stat_value}", True, text_color)  # Keep as string if not a number
        scrollable_surface.blit(stat_text, (icon_x + 40, y_coord + 5))  # Add a small vertical offset for better alignment
        if bar_color:  # Only draw progress bar if bar_color is not None
            pygame.draw.rect(scrollable_surface, (128, 128, 128), (bar_x, y_coord + 30, bar_width, bar_height))  # Adjusted y-coordinate
            fill_width = (stat_value / 100) * bar_width

            # Set bar color based on threshold (if any)
            if threshold is not None and stat_value < threshold:  
                bar_color = (255, 0, 0)  # Red if below threshold

            pygame.draw.rect(scrollable_surface, bar_color, (bar_x, y_coord + 30, fill_width, bar_height))  # Adjusted y-coordinate

        y_coord += icon_height + text_height + bar_height + spacing  # Add spacing

    # --- Round the corners of the stats surface ---
    radius = 20  # Adjust the radius for the desired roundness
    
    # Create a mask with rounded corners
    mask = pygame.Surface((stats_surface_width, total_stats_height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, stats_surface_width, total_stats_height), border_radius=radius)
    
    # Blit the scrollable surface onto the mask
    final_stats_surface = scrollable_surface.copy()
    final_stats_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # --- Tooltips ---
    tooltips = {
        "Name": "The name you gave your Petteomocha.",
        "Age": "How old your Petteomocha is in days.",
        "Hunger": "How hungry your Petteomocha is. Keep it above 30!",
        "Happiness": "How happy your Petteomocha is. Keep it above 30!",
        "Hygiene": "How clean your Petteomocha is.",
        "Energy": "How much energy your Petteomocha has.",
        "Bond": "How strong your bond is with your Petteomocha.",
        "Health": "The overall health of your Petteomocha. Keep it above 30!",
        "Weight": "The weight of your Petteomocha."
    }

    # --- Scroll variables ---
    scroll_y = 0
    scroll_speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks
                clicked_button = buttons.handle_click(event.pos)  # Use your buttons.handle_click()
                if clicked_button == "A":  # A button
                    scroll_y += scroll_speed  # Scroll up
                    scroll_y = min(scroll_y, total_stats_height - stats_surface_height)  # Clamp scroll
                elif clicked_button == "B":  # B button
                    scroll_y -= scroll_speed  # Scroll down
                    scroll_y = max(0, scroll_y)  # Clamp scroll
                elif clicked_button == "C":  # C button
                    running = False  # Exit stats display
            
            # --- Tooltip handling should be inside the event loop ---
            if event.type == pygame.MOUSEMOTION:  # Check for mouse motion
                mouse_pos = event.pos
                # Adjust mouse position for the stats display offset
                adjusted_mouse_pos = (mouse_pos[0] - 135, mouse_pos[1] - 180 + scroll_y)

                y_coord = spacing  # Reset y_coord for each frame

                for stat_name, (stat_value, bar_color, threshold) in stats_data.items():
                    icon_rect = pygame.Rect(icon_x, y_coord, 32, 32)  # Get icon rect
                    if icon_rect.collidepoint(adjusted_mouse_pos):  # Use adjusted position
                            tooltip_text = font.render(tooltips[stat_name], True, text_color)  # Remove the extra parenthesis
                            screen.blit(tooltip_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))  # Position tooltip
                            
                    y_coord += icon_height + text_height + bar_height + spacing  # Update y_coord for the next stat

        # --- Drawing ---
        screen.blit(background_image, (140, 225))
        screen.blit(egg_case_image, (0, 0))

        # --- Apply rounded corners only if not scrolling ---
        if scroll_y == 0:  # Only round corners when at the top
            # Create a mask with rounded corners at the top and bottom
            mask = pygame.Surface((stats_surface_width, total_stats_height), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255), (0, 0, stats_surface_width, total_stats_height), border_top_left_radius=radius, border_top_right_radius=radius, border_bottom_left_radius=radius, border_bottom_right_radius=radius)  # Round all corners

            # Blit the scrollable surface onto the mask
            final_stats_surface = scrollable_surface.copy()
            final_stats_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # Blit the final_stats_surface with rounded corners, scrolling offset and adjusted position
            screen.blit(final_stats_surface, (135, 180), (0, scroll_y, stats_surface_width, stats_surface_height))
        else:  # Blit the original surface with square corners
            screen.blit(scrollable_surface, (135, 180), (0, scroll_y, stats_surface_width, stats_surface_height))

        # Make sure to redraw the buttons!
        buttons.draw_bottom_red_buttons()

        pygame.display.flip()

    print("Exiting stats display...")

    # Redraw the background and monster after closing the stats display
    screen.blit(background_image, (140, 225))
    screen.blit(egg_case_image, (0, 0))
    draw_monster(screen, monster, buttons)

    pygame.display.update()