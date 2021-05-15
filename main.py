import pygame
import os
import time
import random

from pygame.constants import WINDOWCLOSE
# Initializes Font
pygame.font.init()

# Reference: https://www.youtube.com/watch?v=Q-__8Xw9KTM
# Timestamp: 50:21

# Pygame Window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
# Defines the Width and Height and initializes the window and window name

# Load image assets
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
# User Ship
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))

# Projectiles
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# Space Background
SPCBG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.player_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

# Main Loop


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("arial_bold", 50)

    player_vel = 5

    player = Player(370, 450)

    clock = pygame.time.Clock()

    def redraw_window():
        # "Blit" places the defined "SPCBG" into WIN
        WIN.blit(SPCBG, (0, 0))
        # Draws Text
        lives_label = main_font.render(f"Lives: {lives}", 1, (0, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        # Shows Text to "WIN" with BLIT
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # Moves Left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + 50 < WIDTH:  # Moves Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # Moved Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + 50 < HEIGHT:  # Moved Down
            player.y += player_vel
        if keys[pygame.K_q]:  # Quits Game
            run = False


main()
