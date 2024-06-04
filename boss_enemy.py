import pygame
import random
from settings import RED, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from bullet import Bullet
from explosion import Explosion

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, image_path, speed, health, *groups):
        super().__init__(*groups)
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image at {image_path}: {e}")
            raise
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        self.rect = self.image.get_rect()
        print(f"Boss image dimensions: {self.rect.width}x{self.rect.height}")
        self.rect.x = random.randint(0, max(0, SCREEN_WIDTH - self.rect.width))
        self.rect.y = 50
        self.speed = speed
        self.health = health
        self.max_health = health
        self.direction = random.choice([-1, 1])
        self.last_shot = pygame.time.get_ticks()
        self.shoot_interval = 1000
        self.level = 1  # Default level

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_interval:
            self.shoot()
            self.last_shot = current_time

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.explode()
            self.kill()

    def shoot(self):
        bullet_speed = 5
        num_bullets = 3
        if self.level == 2:
            num_bullets = 6
        elif self.level == 3:
            num_bullets = 12

        bullets = []
        for i in range(num_bullets):
            offset_x = i * 20 - (num_bullets // 2) * 20
            bullet = Bullet(self.rect.centerx + offset_x, self.rect.bottom, bullet_speed, RED)
            bullets.append(bullet)

        for bullet in bullets:
            print(f"Boss shooting bullet at x: {bullet.rect.x}, y: {bullet.rect.y}")
            for group in self.groups():
                group.add(bullet)

    def draw_health_bar(self, surface):
        bar_length = self.rect.width
        bar_height = 10
        fill = (self.health / self.max_health) * bar_length
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_length, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(surface, RED, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

    def explode(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        for group in self.groups():
            group.add(explosion)

    def set_level(self, level):
        self.level = level

class FinalBoss(BossEnemy):
    def __init__(self, image_path, speed, health, *groups):
        super().__init__(image_path, speed, health, *groups)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, SCREEN_WIDTH - self.rect.width))
        self.rect.y = 50
        self.shoot_interval = 800  # Shoots more frequently

    def shoot(self):
        bullet_speed = 7
        num_bullets = 18  # Stronger boss shoots more bullets
        bullets = []
        for i in range(num_bullets):
            offset_x = i * 20 - (num_bullets // 2) * 20
            bullet = Bullet(self.rect.centerx + offset_x, self.rect.bottom, bullet_speed, RED)
            bullets.append(bullet)

        for bullet in bullets:
            print(f"Final Boss shooting bullet at x: {bullet.rect.x}, y: {bullet.rect.y}")
            for group in self.groups():
                group.add(bullet)
