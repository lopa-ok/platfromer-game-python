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
POWER_UP_SIZE = 30
PLAYER_HEALTH = 3
LEVEL_DURATION = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

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
        self.health = PLAYER_HEALTH
        self.invincible = False
        self.invincibility_timer = 0

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
        if coins_hit:
            self.score += len(coins_hit)

        # Collect power-ups
        power_ups_hit = pygame.sprite.spritecollide(self, power_ups, True)
        if power_ups_hit:
            self.invincible = True
            self.invincibility_timer = FPS * 5

        # Invincibility countdown
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False

        # Collision with enemies
        if not self.invincible and pygame.sprite.spritecollide(self, enemies, False):
            self.health -= 1
            if self.health <= 0:
                self.kill()

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, move_x=0, move_y=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = move_x
        self.move_y = move_y
        self.direction_x = 1
        self.direction_y = 1

    def update(self):
        if self.move_x:
            self.rect.x += self.move_x * self.direction_x
            if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
                self.direction_x *= -1

        if self.move_y:
            self.rect.y += self.move_y * self.direction_y
            if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
                self.direction_y *= -1

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

# Power-Up
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((POWER_UP_SIZE, POWER_UP_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Group for sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
power_ups = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create platforms
platform_list = [
    (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
    (150, 400, 200, 20),
    (400, 300, 200, 20),
    (250, 200, 200, 20, 2, 0),
    (600, 500, 200, 20, 0, 2),
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

# Create power-ups
for i in range(2):
    power_up = PowerUp(random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE), random.randint(0, SCREEN_HEIGHT - POWER_UP_SIZE))
    power_ups.add(power_up)
    all_sprites.add(power_up)


# Game Loop
running = True
level_timer = LEVEL_DURATION * FPS
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not player.alive():
            if event.key == pygame.K_r:
                # Restart the game
                player = Player()
                all_sprites.add(player)
                running = True

    # Update
    if player.alive():
        all_sprites.update()

    # Collision with platforms
    if pygame.sprite.spritecollide(player, platforms, False):
        player.rect.bottom = platform.rect.top
        player.vel_y = 0
        player.jumping = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw score and health
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))

    
    level_timer -= 1
    if level_timer <= 0:
        level_timer = LEVEL_DURATION * FPS
        new_enemy = Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 20)
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    if not player.alive():
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    
    # Flip the screen
    pygame.display.flip()

pygame.quit()
