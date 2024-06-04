import pygame
from bullet import Bullet
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, image, shoot_sound, width, height):
        super().__init__()
        self.original_image = pygame.transform.scale(image, (width, height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0
        self.shoot_sound = shoot_sound
        self.health = 100
        self.bullet_speed = 10  # Initial bullet speed
        self.power_up = None
        self.power_up_end_time = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.power_up and pygame.time.get_ticks() > self.power_up_end_time:
            self.power_up = None

    def shoot(self, all_sprites, bullets):
        if self.power_up == 'double':
            bullet1 = Bullet(self.rect.centerx - 10, self.rect.top, -self.bullet_speed, GREEN)
            bullet2 = Bullet(self.rect.centerx + 10, self.rect.top, -self.bullet_speed, GREEN)
            all_sprites.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top, -self.bullet_speed, GREEN)
            all_sprites.add(bullet)
            bullets.add(bullet)
        self.shoot_sound.play()

    def apply_power_up(self, power_up):
        self.power_up = power_up
        self.power_up_end_time = pygame.time.get_ticks() + 5000  # Power-up lasts for 5 seconds

    def level_up(self):
        self.bullet_speed += BULLET_SPEED_INCREMENT

    def apply_health_potion(self):
        self.health = min(self.health + 20, 100)  # Increase health by 20, max 100
