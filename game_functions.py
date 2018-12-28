import sys

import pygame
def check_events() -> None:
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def update_screen(ai_settings, screen, ship) -> None:
    """Update images on the screen and flip to new screen"""
    # redraw the screen during each pass through loop
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # make the most recently drawn screen visible
    pygame.display.flip()