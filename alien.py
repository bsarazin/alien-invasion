import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """space monster!"""

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Load the alien image and set its Rect attributes
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self) -> None:
        """Draw the alien at it's current location"""
        self.screen.blit(self.image, self.rect)
