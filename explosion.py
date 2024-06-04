import pygame
from settings import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)  # Simple red square for explosion
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.start_time = pygame.time.get_ticks()
        self.duration = 500  # Explosion lasts for 0.5 seconds

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()
