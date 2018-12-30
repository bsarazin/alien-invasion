import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions


def run_game():
    # initialize and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # create a Ship object, make groups to store bullets, aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # create alien fleet
    game_functions.create_fleet(ai_settings, screen, ship, aliens)

    # start the main loop
    while True:
        game_functions.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        game_functions.update_bullets(bullets)
        # game_functions.update_aliens(aliens)
        game_functions.update_aliens(ai_settings, aliens)
        game_functions.update_screen(
            ai_settings, screen, ship, aliens, bullets)


run_game()
