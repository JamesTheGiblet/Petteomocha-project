# boundary_restriction.py

import random

def restrict_to_background(element_rect, background_rect):
    """Restricts the given element's rect to be within the background rect."""
    element_rect.x = max(background_rect.left, min(element_rect.x, background_rect.right - element_rect.width))
    element_rect.y = max(background_rect.top, min(element_rect.y, background_rect.bottom - element_rect.height))

def generate_position_within_background(element_width, element_height, background_rect):
    """Generates a random position within the background rect for an element of the given size."""
    x = random.randint(background_rect.left, background_rect.right - element_width)
    y = random.randint(background_rect.top, background_rect.bottom - element_height)
    return x, y
