# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player settings
PLAYER_WIDTH_LARGE = 100
PLAYER_HEIGHT_LARGE = 105
PLAYER_WIDTH_SMALL = 50
PLAYER_HEIGHT_SMALL = 75
player_speed = 5

# Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 3

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7

LEVEL_THRESHOLDS = [25, 50, 100, 150]  # Scores at which the player levels up
BULLET_SPEED_INCREMENT = 2  # Increase bullet speed by this value each level up
ENEMY_SPEED_INCREMENT = 0.5  # Increase enemy speed by this value each level up
ENEMY_COUNT_INCREMENT = 1  # Increase enemy count by this value each level up
STAR_IMAGE_PATH = "images/star.png"  # Path to star image

# Boss enemy settings
BOSS_THRESHOLD = 200  # Score at which the boss enemy appears
BOSS_SPEED = 2  # Speed of the boss enemy
BOSS_HEALTH = 300  # Health of the boss enemy
BOSS_ENEMY_IMAGE_PATH = "images/boss.png"  # Path to boss enemy image
BOSS_APPEAR_SOUND_PATH = "sounds/little-alien-142498.mp3"  # Sound for boss appearance

# Difficulty levels
difficulty_increase_interval = 5000  # Interval for difficulty increase (ms)
last_difficulty_increase = 0

POWER_UP_SCORE_INTERVAL = 50  # Power-up will appear every 50 points

# Difficulty levels and settings
difficulty_levels = ["Easy", "Medium", "Hard"]
difficulty_settings = [
    {"enemy_count": 3, "enemy_speed": 1},  # Easy
    {"enemy_count": 5, "enemy_speed": 2},  # Medium
    {"enemy_count": 7, "enemy_speed": 3},  # Hard
]
difficulty_index = 1  # Default difficulty "Medium"

# Initial enemy count and speed
initial_enemy_count = difficulty_settings[difficulty_index]["enemy_count"]
initial_enemy_speed = difficulty_settings[difficulty_index]["enemy_speed"]
current_enemy_speed = initial_enemy_speed
current_enemy_count = initial_enemy_count

# Sound settings
volume = 0.5  # Default volume level

# Image file paths
PLAYER_IMAGE_PATH = "images/transparent_arcade_spaceship.png"
ENEMY_IMAGE_PATH = "images/pngwing.com-4.png"
BACKGROUND_IMAGE_PATH = "images/as.png"
POWER_UP_IMAGE_PATH = "images/bolt.png"
HEALTH_POTION_IMAGE_PATH = "images/health_potion.png"  # Path to health potion image
# Final boss image path
FINAL_BOSS_IMAGE_PATH = "images/final_boss.png"
# High score file path
HIGH_SCORE_FILE = "high_score.txt"

# Sound file paths
SHOOT_SOUND_PATH = "sounds/laser-104024.mp3"
ENEMY_HIT_SOUND_PATH = "sounds/rock-break-183794.mp3"
MUSIC_PATH = "sounds/interstellar-dark-trailer-161065.mp3"
POWER_UP_SOUND_PATH = "sounds/coin-upaif-14631.mp3"
HEALTH_POTION_SOUND_PATH = "sounds/health_potion.mp3"  # Path to health potion sound
