# health_potion.py
import random
import pygame

from settings import *

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)  # Start above the screen
        self.speedy = random.randint(1, 5)  # Random falling speed

    def update(self):
        self.rect.y += self.speedy
        # Kill the potion if it moves off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
