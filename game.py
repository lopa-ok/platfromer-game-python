import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 3
COIN_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

# Clock
clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 36)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_y = 0
        self.jumping = False
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Check if player is on the ground
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.jumping = False

        # Jump
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = JUMP_STRENGTH
            self.jumping = True

        # Collect coins
        coins_hit = pygame.sprite.spritecollide(self, coins, True)
        self.score += len(coins_hit)

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1

# Coin
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Group for sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create platforms
platform_list = [
    (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
    (150, 400, 200, 20),
    (400, 300, 200, 20),
    (250, 200, 200, 20),
]

for plat in platform_list:
    platform = Platform(*plat)
    platforms.add(platform)
    all_sprites.add(platform)

# Create enemies
enemy = Enemy(150, 360, 50, 20)
enemies.add(enemy)
all_sprites.add(enemy)

# Create coins
for i in range(5):
    coin = Coin(random.randint(0, SCREEN_WIDTH - COIN_SIZE), random.randint(0, SCREEN_HEIGHT - COIN_SIZE))
    coins.add(coin)
    all_sprites.add(coin)

# Game Loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Collision
    if pygame.sprite.spritecollide(player, platforms, False):
        player.rect.bottom = platform.rect.top
        player.vel_y = 0
        player.jumping = False
    if pygame.sprite.spritecollide(player, enemies, False):
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Flip the display
    pygame.display.flip()

pygame.quit()
