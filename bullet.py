import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = speed  # Bullet direction and speed
        self.color = color  # Save color for collision detection

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
