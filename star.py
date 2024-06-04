# star.py
import random
import pygame

from settings import *

class Star(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.original_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def update(self):
        pass  # Stars don't move in this implementation
