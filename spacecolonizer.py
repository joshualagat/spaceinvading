import pygame
import os
import time
import random
from pygame.constants import WINDOWCLOSE
from pygame import mixer
# Initializes Font
pygame.font.init()
# Initializes mixer (music)
pygame.mixer.init()

# Made by: Joshua Lagat

# Pygame Window
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Colonizers")
# Defines the Width and Height and initializes the window and window name

# Main Menu Font
main_font = pygame.font.Font("assets/font/joystix monospace.ttf", 25)
#os.path.join("assets", "joystix monospace.ttf", 25)

# Sounds
laser_sound = mixer.Sound("assets/sound/laser.wav")
explosion_sound = mixer.Sound("assets/sound/explosion.wav")
pop_sound = mixer.Sound("assets/sound/pop.wav")
gameover_sound = mixer.Sound("assets/sound/gameover.wav")
bruh_sound = mixer.Sound("assets/sound/bruh.wav")

# Game Icon
GAME_ICON = pygame.image.load(
    os.path.join("assets", "icon.png"))
pygame.display.set_icon(GAME_ICON)

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

# Background Music
mixer.music.load("assets/sound/background-music.wav")
mixer.music.play(-1)

# Laser


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# Ship


class Ship:
    COOLDOWN = 30

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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
                explosion_sound.play()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            laser_sound.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_width()

# Player


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.player_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        explosion_sound.play()
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +
                         10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

# Enemy


class Enemy(Ship):
    # COLOR_MAP is a dictionary where it defines which spaceships and lasers go where using strings.
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        pop_sound.play()
        # This calls on color_map to define the ships using strings that are in a dictionary.
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        laser_sound.play()
        if self.cool_down_counter == 0:
            laser = Laser(self.x-24, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# Collision Loop


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Uses map.overlap to identify if there are overlapping pixels.
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Main Loop


def main():
    run = True
    FPS = 360
    level = 0
    lives = 5
    main_font = pygame.font.Font("assets/font/joystix monospace.ttf", 40)
    lost_font = pygame.font.Font("assets/font/joystix monospace.ttf", 45)

    enemies = []
    wave_length = 2
    enemy_vel = 2

    player_vel = 14
    laser_vel = 12

    player = Player(350, 400)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        # "Blit" places the defined "SPCBG" into WIN
        WIN.blit(SPCBG, (0, 0))
        # Draws Text
        lives_label = main_font.render(f"Lives: {lives}", 1, (0, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        # Shows Text to "WIN" with BLIT
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        # Lost Screen
        if lost:
            gameover_sound.play()
            lost_label = lost_font.render("You Lost, loser!", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 0.25:
                pop_sound.play()
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 3
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100),
                              random.randrange(-1500*level/5, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # Move Left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # Move Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # Move Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # Move Down
            player.y += player_vel
        if keys[pygame.K_SPACE]:  # Shoots Lasers
            player.shoot()
        if keys[pygame.K_q]:  # Quits Game
            run = False

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                explosion_sound.play()
                bruh_sound.play()
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


def main_menu():
    run = True
    while run:
        WIN.blit(SPCBG, (0, 0))
        menu_label = main_font.render(
            "Press any mouse key to start...", 1, (255, 255, 255))
        WIN.blit(menu_label, (WIDTH/2 - menu_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    quit()


main_menu()
