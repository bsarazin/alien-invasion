import sys
import pygame
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets) -> None:
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y) -> None:
    """Start a new game when user clicks Play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # Empty the lists of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets) -> None:
    """Respond to key presses"""
    if event.key == pygame.K_RIGHT:
        # Move ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the group
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship) -> None:
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button) -> None:
    """Update images on the screen and flip to new screen"""
    # redraw the screen during each pass through loop
    screen.fill(ai_settings.bg_color)

    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets) -> None:
    """Update the positions of bullets and remove old bullets"""
    bullets.update()
    remove_bullets(bullets)
    check_bullet_alien_collisions(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets)


def remove_bullets(bullets) -> None:
    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets) -> None:
    """Respond to any bullet collisions"""
    # Check for any bullets that have hit aliens
    # If so, get rid of the bullet and the alien
    # stored in a Dictionary
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        # Increase level
        stats.level += 1
        scoreboard.prep_level()


def fire_bullet(ai_settings, screen, ship, bullets) -> None:
    """Fires bullet if limit not reached"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens) -> None:
    """Create a shit ton of aliens"""
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is equal to one alien
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien)
    number_aliens_y = get_number_aliens_y(ai_settings, ship, alien)

    # Create a fleet of aliens
    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien) -> int:
    """Determine the number of aliens that fit in a row"""
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_aliens_y(ai_settings, ship, alien) -> int:
    """Determine the number of rows of aliens"""
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


def create_alien(ai_settings, screen, aliens, alien_number, row_number) -> None:
    """Create a fleet of aliens"""
    # Create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def update_aliens(ai_settings, stats, screen, scoreboard, ship, aliens, bullets) -> None:
    """Check if the fleet is at an edge, and then update the position of all aliens"""
    check_aliens_bottom(ai_settings, stats, screen,
                        scoreboard, ship, aliens, bullets)
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen, scoreboard, ship, aliens, bullets) -> None:
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as a collision
            ship_hit(ai_settings, stats, screen,
                     scoreboard, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens) -> None:
    """Return true if ANY of the aliens is at the edge of screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens) -> None:
    """Drop the entire fleet and change the fleet direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets) -> None:
    """Respond to a ship being hit"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Updated scoreboard
        scoreboard.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new ship and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, scoreboard) -> None:
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
