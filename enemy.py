import pygame
import random
from settings import enemy_width, enemy_height, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, enemies):
        super(Enemy, self).__init__()
        self.image = pygame.transform.scale(image, (enemy_width, enemy_height))
        self.rect = self.image.get_rect()
        self.speed_y = speed
        self.acceleration = 0.01  # Hızlanma faktörü
        self.mask = pygame.mask.from_surface(self.image)  # Mask oluştur
        self.enemies = enemies
        self.rect.x, self.rect.y = self.get_non_overlapping_position()

    def get_non_overlapping_position(self):
        max_attempts = 100  # Maksimum deneme sayısı
        for _ in range(max_attempts):
            x = random.randint(0, SCREEN_WIDTH - enemy_width)
            y = random.randint(-100, -40)
            self.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(self, self.enemies, pygame.sprite.collide_mask):
                return x, y
        # Eğer maksimum deneme sayısına ulaşıldıysa rastgele bir pozisyon döndür
        return random.randint(0, SCREEN_WIDTH - enemy_width), random.randint(-100, -40)

    def update(self):
        self.rect.y += self.speed_y
        self.speed_y += self.acceleration  # Her çerçevede hızı artır
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x, self.rect.y = self.get_non_overlapping_position()
            self.speed_y = 3  # Yeniden başlarken hızı resetle
