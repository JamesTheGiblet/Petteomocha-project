# movement.py


def update_monster_movement(monster, dt, screen):
    """Updates the monster's position and movement."""

    if not monster.is_sleeping:  # Only move if not sleeping
        monster.x += monster.speed * monster.direction[0] * dt  # Scale movement with dt
        monster.y += monster.speed * monster.direction[1] * dt  # Scale movement with dt

        # --- Keep monster within the defined box ---
        box_x = 145  # Updated x-coordinate
        box_y = 370  # Updated y-coordinate
        box_width = 430 - box_x  # Updated width
        box_height = 440 - box_y  # Updated height

        monster_rect = monster.image.get_rect(center=(monster.x, monster.y))

        if monster.x < box_x or monster.x > box_x + box_width - monster_rect.width:
            monster.direction[0] *= -1  # Reverse x-direction
        if monster.y < box_y or monster.y > box_y + box_height - monster_rect.height:
            monster.direction[1] *= -1  # Reverse y-direction
            
    # --- Draw red border for testing ---
    # Moved outside the if block to always draw the border
#    pygame.draw.rect(screen, (255, 0, 0), (box_x, box_y, box_width, box_height), 2)  # Add this line
