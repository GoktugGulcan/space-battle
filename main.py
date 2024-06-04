import random
import pygame
import os
from settings import *
from player import Player
from enemy import Enemy
from boss_enemy import BossEnemy, FinalBoss
from powerup import PowerUp
from health_potion import HealthPotion
from star import Star
from bullet import Bullet
from explosion import Explosion

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound files
shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
enemy_hit_sound = pygame.mixer.Sound(ENEMY_HIT_SOUND_PATH)
power_up_sound = pygame.mixer.Sound(POWER_UP_SOUND_PATH)
health_potion_sound = pygame.mixer.Sound(POWER_UP_SOUND_PATH)
boss_appear_sound = pygame.mixer.Sound(BOSS_APPEAR_SOUND_PATH)
shoot_sound.set_volume(volume)
enemy_hit_sound.set_volume(volume)
power_up_sound.set_volume(volume)
health_potion_sound.set_volume(volume)
boss_appear_sound.set_volume(volume)

# Load music and play
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Battle")

# Load images
player_large_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
player_small_image = pygame.image.load(POWER_UP_IMAGE_PATH).convert_alpha()
enemy_image = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()
boss_enemy_image = pygame.image.load(BOSS_ENEMY_IMAGE_PATH).convert_alpha()
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
menu_background_image = pygame.image.load("images/as.png").convert()
star_image = STAR_IMAGE_PATH
health_potion_image = "images/health_potion.png"

# Clock
clock = pygame.time.Clock()

# Reset level thresholds for new game
def reset_level_thresholds():
    global LEVEL_THRESHOLDS
    LEVEL_THRESHOLDS = [25, 50, 100, 150]

def load_high_score():
    if not os.path.isfile(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as file:
        try:
            return int(file.read().strip())
        except ValueError:
            return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def reset_game():
    global all_sprites, enemies, bullets, power_ups, health_potions, player, score, current_enemy_speed, current_enemy_count, last_difficulty_increase, next_level_threshold, bosses, boss_active
    reset_level_thresholds()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    health_potions = pygame.sprite.Group()
    bosses = pygame.sprite.Group()

    player = Player(player_large_image, shoot_sound, width=PLAYER_WIDTH_LARGE, height=PLAYER_HEIGHT_LARGE)
    all_sprites.add(player)

    current_enemy_speed = difficulty_settings[difficulty_index]["enemy_speed"]
    current_enemy_count = difficulty_settings[difficulty_index]["enemy_count"]

    for _ in range(current_enemy_count):
        enemy = Enemy(enemy_image, current_enemy_speed, enemies)
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    next_level_threshold = LEVEL_THRESHOLDS.pop(0) if LEVEL_THRESHOLDS else None
    last_difficulty_increase = pygame.time.get_ticks()
    boss_active = False

def game_loop():
    global running, high_score, score, last_difficulty_increase, current_enemy_speed, current_enemy_count, next_level_threshold, boss_active

    running = True
    background_y = 0  # For scrolling background

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets)

        all_sprites.update()

        # Scroll background
        background_y += 1
        if background_y >= SCREEN_HEIGHT:
            background_y = 0

        # Handle collisions
        if not boss_active:
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 1
                enemy_hit_sound.play()
                enemy = Enemy(enemy_image, current_enemy_speed, enemies)
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Handle player bullets hitting the boss
        boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
        for boss, hits in boss_hits.items():
            if isinstance(boss, BossEnemy) or isinstance(boss, FinalBoss):
                for hit in hits:
                    boss.take_damage(10)  # Adjust damage as needed

        # Handle boss bullets hitting the player
        player_hits = pygame.sprite.spritecollide(player, bullets, True)
        for hit in player_hits:
            if hit.color == RED:  # Ensure only boss bullets damage the player
                player.health -= 40  # Reduce health by 40 for each hit
                if player.health <= 0:
                    running = False  # End game if player's health is 0 or less

        # Handle boss appearance and removal of enemies
        if next_level_threshold and score >= next_level_threshold:
            if not boss_active:
                # Remove all meteors
                for enemy in enemies:
                    enemy.kill()

                # Spawn the boss
                if score >= 150:
                    boss = FinalBoss(FINAL_BOSS_IMAGE_PATH, BOSS_SPEED + 2, BOSS_HEALTH * 5, bosses)
                elif score >= 100:
                    boss = BossEnemy(BOSS_ENEMY_IMAGE_PATH, BOSS_SPEED + 2, BOSS_HEALTH * 3, bosses)
                    boss.set_level(3)
                elif score >= 50:
                    boss = BossEnemy(BOSS_ENEMY_IMAGE_PATH, BOSS_SPEED + 1, BOSS_HEALTH * 2, bosses)
                    boss.set_level(2)
                else:
                    boss = BossEnemy(BOSS_ENEMY_IMAGE_PATH, BOSS_SPEED, BOSS_HEALTH, bosses)
                    boss.set_level(1)
                
                all_sprites.add(boss)
                bosses.add(boss)
                boss_appear_sound.play()
                boss_active = True

            if boss_active and not bosses:
                if isinstance(boss, FinalBoss):
                    success_screen()
                    running = False
                else:
                    # Boss defeated
                    boss_active = False
                    next_level_threshold = LEVEL_THRESHOLDS.pop(0) if LEVEL_THRESHOLDS else None
                    current_enemy_speed += ENEMY_SPEED_INCREMENT
                    current_enemy_count += ENEMY_COUNT_INCREMENT

                    for _ in range(current_enemy_count):
                        enemy = Enemy(enemy_image, current_enemy_speed, enemies)
                        all_sprites.add(enemy)
                        enemies.add(enemy)

        current_time = pygame.time.get_ticks()
        if current_time - last_difficulty_increase > difficulty_increase_interval:
            last_difficulty_increase = current_time
            current_enemy_speed += 0.5
            if current_enemy_count < 10 and not boss_active:
                enemy = Enemy(enemy_image, current_enemy_speed, enemies)
                all_sprites.add(enemy)
                enemies.add(enemy)
                current_enemy_count += 1

        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(player, bosses, False, pygame.sprite.collide_mask):
            player.health -= 30
            for enemy in enemies:
                if pygame.sprite.collide_mask(player, enemy):
                    enemy.kill()
            for boss in bosses:
                if isinstance(boss, BossEnemy) or isinstance(boss, FinalBoss):
                    if pygame.sprite.collide_mask(player, boss):
                        boss.take_damage(30)
                        if boss.health <= 0:
                            boss.explode()
                            boss.kill()
                            if isinstance(boss, FinalBoss):
                                success_screen()
                                running = False
                            else:
                                # Restore normal mode
                                boss_active = False
                                next_level_threshold = LEVEL_THRESHOLDS.pop(0) if LEVEL_THRESHOLDS else None
                                current_enemy_speed += ENEMY_SPEED_INCREMENT
                                current_enemy_count += ENEMY_COUNT_INCREMENT

                                for _ in range(current_enemy_count):
                                    enemy = Enemy(enemy_image, current_enemy_speed, enemies)
                                    all_sprites.add(enemy)
                                    enemies.add(enemy)

            if player.health <= 0:
                running = False

        # Spawn power-ups and health potions randomly
        if random.randint(1, 500) == 1:
            power_up = PowerUp(player_small_image, width=PLAYER_WIDTH_SMALL, height=PLAYER_HEIGHT_SMALL)
            all_sprites.add(power_up)
            power_ups.add(power_up)

        if random.randint(1, 1000) == 1:
            health_potion = HealthPotion(health_potion_image, 30, 30)
            all_sprites.add(health_potion)
            health_potions.add(health_potion)

        power_up_hits = pygame.sprite.spritecollide(player, power_ups, True)
        for hit in power_up_hits:
            power_up_sound.play()
            player.apply_power_up('double')

        health_potion_hits = pygame.sprite.spritecollide(player, health_potions, True)
        for hit in health_potion_hits:
            health_potion_sound.play()
            player.apply_health_potion()

        screen.fill(BLACK)
        screen.blit(background_image, (0, background_y - SCREEN_HEIGHT))
        screen.blit(background_image, (0, background_y))
        all_sprites.draw(screen)
        for boss in bosses:
            if isinstance(boss, BossEnemy) or isinstance(boss, FinalBoss):
                boss.draw_health_bar(screen)
        draw_text(screen, f'Score: {score}', 36, 10, 10, WHITE)
        draw_text(screen, f'Health: {player.health}', 36, 10, 50, WHITE)
        pygame.display.flip()
        clock.tick(60)

    if score > high_score:
        high_score = score
        save_high_score(high_score)




def success_screen():
    font_large = pygame.font.SysFont(None, 72)
    text_large = font_large.render("You Win!", True, GREEN)
    text_rect = text_large.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_large, text_rect)

    font_medium = pygame.font.SysFont(None, 48)
    text_medium = font_medium.render(f"Score: {score}", True, WHITE)
    text_rect_medium = text_medium.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text_medium, text_rect_medium)

    font_small = pygame.font.SysFont(None, 36)
    high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(high_score_text, high_score_rect)

    pygame.display.flip()
    pygame.time.wait(5000)

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def game_over_screen():
    font_large = pygame.font.SysFont(None, 72)
    text_large = font_large.render("Game Over", True, RED)
    text_rect = text_large.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_large, text_rect)

    font_medium = pygame.font.SysFont(None, 48)
    text_medium = pygame.font.SysFont(None, 48).render(f"Score: {score}", True, WHITE)
    text_rect_medium = text_medium.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text_medium, text_rect_medium)

    font_small = pygame.font.SysFont(None, 36)
    high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(high_score_text, high_score_rect)

    try_again_text = font_small.render("Press 'R' to Try Again", True, WHITE)
    try_again_rect = try_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(try_again_text, try_again_rect)

    # Display stars based on score
    if score >= 500:
        num_stars = 3
    elif score >= 150:
        num_stars = 2
    elif score >= 20:
        num_stars = 1
    else:
        num_stars = 0

    for i in range(num_stars):
        star = Star(star_image, 50, 50)
        star.rect.center = (SCREEN_WIDTH // 2 - 60 + i * 60, SCREEN_HEIGHT // 2 - 100)
        screen.blit(star.image, star.rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
    return False

def settings_screen():
    global volume, difficulty_index
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and volume < 1.0:
                    volume += 0.1
                    pygame.mixer.music.set_volume(volume)
                    shoot_sound.set_volume(volume)
                    enemy_hit_sound.set_volume(volume)
                elif event.key == pygame.K_DOWN and volume > 0.0:
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)
                    shoot_sound.set_volume(volume)
                    enemy_hit_sound.set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    difficulty_index = (difficulty_index + 1) % len(difficulty_levels)
                elif event.key == pygame.K_LEFT:
                    difficulty_index = (difficulty_index - 1) % len(difficulty_levels)
                elif event.key == pygame.K_b:
                    settings_running = False

        volume_text = font.render(f"Volume: {int(volume * 100)}", True, WHITE)
        difficulty_text = font.render(f"Difficulty: {difficulty_levels[difficulty_index]}", True, WHITE)
        back_text = small_font.render("Back (B)", True, WHITE)

        volume_rect = volume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.fill(BLACK)
        screen.blit(volume_text, volume_rect)
        screen.blit(difficulty_text, difficulty_rect)
        screen.blit(back_text, back_rect)
        pygame.display.flip()

    reset_game()
    return True

def main_menu():
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)

    title_text = font_large.render("Space Battle", True, (255, 0, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    play_text = font_medium.render("Start", True, (0, 255, 0))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    settings_text = font_medium.render("Settings", True, (0, 0, 255))
    settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

    credits_text = font_small.render("Press Start to Begin", True, (255, 255, 255))
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_m:
                    if not settings_screen():
                        return False

        screen.fill((0, 0, 0))
        screen.blit(menu_background_image, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(settings_text, settings_rect)
        screen.blit(credits_text, credits_rect)
        pygame.display.flip()

    return False

def main():
    global high_score
    high_score = load_high_score()
    while True:
        if not main_menu():
            break
        reset_game()
        game_loop()
        if not game_over_screen():
            break

    pygame.quit()

if __name__ == "__main__":
    main()

