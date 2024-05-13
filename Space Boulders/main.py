import sys
import os
import pygame
import random

from data.models.classes.asteroid import Asteroid
from data.models.classes.asteroidClassDataTransferModel import AsteroidClassDataTransferModel
from data.models.classes.checkWhichKeyPressedDataTransferModel import CheckWhichKeyPressedDataTransferModel
from data.models.classes.live import Live
from data.models.classes.projectile import Projectile
from data.models.classes.ship import Ship
from data.models.classes.shipCollisionsDataModel import ShipsCollisionsDataModel
from data.models.classes.ufo import UFO
from data.models.classes.ufoUpdateDataModel import UfoUpdateDataModel
from data.models.classes.button import Button

pygame.init()

WIDTH, HEIGHT = 800, 600
PROJECTILE_RADIUS = 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Boulders")
BG = pygame.transform.scale(pygame.image.load("data/assets/sprites/bg.png"), (WIDTH, HEIGHT))

SHIP_ROTATION_VEL = 4

ASTEROID_1_BASE_VEL, ASTEROID_2_BASE_VEL, ASTEROID_3_BASE_VEL = 3, 4, 5
POINT_VALUE_ASTEROID_1, POINT_VALUE_ASTEROID_2, POINT_VALUE_ASTEROID_3 = 200, 500, 1000
ASTEROID_1_IMAGE, ASTEROID_2_IMAGE, ASTEROID_3_IMAGE = (
    'data/assets/sprites/Asteroid_1.png', 'data/assets/sprites/Asteroid_2.png', 'data/assets/sprites/Asteroid_3.png')
(MAX_ASTEROID_1_WIDTH, MAX_ASTEROID_1_HEIGHT, MAX_ASTEROID_2_WIDTH, MAX_ASTEROID_2_HEIGHT, MAX_ASTEROID_3_WIDTH,
 MAX_ASTEROID_3_HEIGHT) = 80, 80, 60, 60, 40, 40

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

PROJECTILE_ADD_INCREMENT = 5
PROJECTILE_COOLDOWN = 200
HYPER_SPACE_COOLDOWN = 500
UFO_PROJECTILE_COOLDOWN = 1_000
UFO_COOLDOWN = 10_000

MAX_DISTANCE_FROM_BORDER_ASTEROID_SPAWNING = 100
ASTEROID_AMOUNT = 5
LIVE_AMOUNT = 5

TRANSFER_DATA_ASTEROID_1 = AsteroidClassDataTransferModel(ASTEROID_1_BASE_VEL, POINT_VALUE_ASTEROID_1,
                                                          ASTEROID_1_IMAGE,
                                                          (MAX_ASTEROID_1_WIDTH, MAX_ASTEROID_1_HEIGHT),
                                                          1)
TRANSFER_DATA_ASTEROID_2 = AsteroidClassDataTransferModel(ASTEROID_2_BASE_VEL, POINT_VALUE_ASTEROID_2,
                                                          ASTEROID_2_IMAGE,
                                                          (MAX_ASTEROID_2_WIDTH, MAX_ASTEROID_2_HEIGHT),
                                                          2)
TRANSFER_DATA_ASTEROID_3 = AsteroidClassDataTransferModel(ASTEROID_3_BASE_VEL, POINT_VALUE_ASTEROID_3,
                                                          ASTEROID_3_IMAGE,
                                                          (MAX_ASTEROID_3_WIDTH, MAX_ASTEROID_3_HEIGHT),
                                                          3)

SCORE_FONT = pygame.font.SysFont('Arial', 30)
HIGH_SCORE_FONT = pygame.font.SysFont('Arial', 15)

REPLAY_BUTTON = Button(250, 400, 150, 50, WHITE, "Replay")
QUIT_BUTTON = Button(400, 400, 150, 50, WHITE, "Quit")
START_BUTTON = Button(300, 300, 200, 50, WHITE, "Start")

CLICK_EFFECT = pygame.mixer.Sound('data/assets/sfx/click.wav')
HIT_EFFECT = pygame.mixer.Sound('data/assets/sfx/hit.wav')
LASER_SHOOT_EFFECT = pygame.mixer.Sound('data/assets/sfx/laserShoot.wav')
LIVE_LOST_EFFECT = pygame.mixer.Sound('data/assets/sfx/liveLost.wav')
NEW_HIGH_SCORE_EFFECT = pygame.mixer.Sound('data/assets/sfx/newHighScore.wav')


def main():
    run = True
    game_over = False
    start_menu = True

    clock = pygame.time.Clock()

    live_amount = LIVE_AMOUNT
    last_projectile_time = 0
    last_hyper_space_time = 0
    last_ufo_projectile_time = 0
    last_ufo_time = 0

    ship = Ship()
    ufo = UFO()

    projectiles = []
    asteroids_sets = [[], [], []]
    ufo_projectiles = []

    points = 0
    high_score = read_high_score()

    while run:
        while start_menu:
            draw_start_menu(high_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if START_BUTTON.is_clicked(mouse_pos):
                        CLICK_EFFECT.play()
                        start_menu = False

        lives = []

        clock.tick(60)
        current_time = pygame.time.get_ticks()

        run = check_for_quit_event_and_continue()
        high_score = update_high_score(points, high_score)

        check_for_ship_collisions_data_model = ShipsCollisionsDataModel(ship, asteroids_sets, ufo_projectiles)
        return_data = check_for_ship_collisions(check_for_ship_collisions_data_model)
        ship_collided = return_data.ship
        asteroids_sets = return_data.asteroids_sets
        ufo_projectiles = return_data.ufo_projectiles
        if ship_collided:
            live_amount -= 1
            LIVE_LOST_EFFECT.play()

        if asteroids_sets[0] == [] and asteroids_sets[1] == [] and asteroids_sets[2] == []:
            new_asteroids = []
            for _ in range(ASTEROID_AMOUNT):
                new_asteroids.append(create_new_asteroid(TRANSFER_DATA_ASTEROID_1, None, None, None))
            asteroids_sets[0] = new_asteroids

        ufo_update_transfer_model = UfoUpdateDataModel(ufo, last_ufo_time)
        ufo_return_data = handle_ufo(ufo_update_transfer_model)
        ufo = ufo_return_data.ufo
        last_ufo_time = ufo_return_data.last_ufo_time
        if current_time - last_ufo_projectile_time >= UFO_PROJECTILE_COOLDOWN:
            last_ufo_projectile_time = current_time
            ufo_projectiles = shoot_ufo_projectile(ufo, ufo_projectiles)

        live_x = WIDTH / 4 * 3
        for _ in range(live_amount):
            live = Live((live_x, 30))
            lives.append(live)
            live_x += live.live_rect.width

        if len(lives) == 0:
            game_over = True

        transfer_data = CheckWhichKeyPressedDataTransferModel(ship, last_hyper_space_time, last_projectile_time,
                                                              projectiles)
        return_data = check_which_key_pressed(transfer_data)
        ship = return_data.ship
        last_hyper_space_time = return_data.last_hyper_space_time
        last_projectile_time = return_data.last_projectile_time
        projectiles = return_data.projectiles

        projectiles, ufo_projectiles = move_all_projectiles(projectiles, ufo_projectiles)

        asteroids_sets = move_all_asteroids(asteroids_sets)

        projectiles, asteroids_sets, ufo, points = check_for_projectile_collisions(projectiles, asteroids_sets, ufo,
                                                                                   points)

        updated_ship = pygame.transform.rotate(ship.original_ship, ship.ship_angle)
        ship_rect = updated_ship.get_rect(center=ship.ship_rect.center)

        draw(updated_ship, ship_rect, projectiles, lives, asteroids_sets, ufo, ufo_projectiles, points, high_score)

        while game_over:
            draw_game_over_screen(high_score, points)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if REPLAY_BUTTON.is_clicked(mouse_pos):
                        CLICK_EFFECT.play()
                        live_amount = LIVE_AMOUNT
                        last_projectile_time = 0
                        last_hyper_space_time = 0
                        last_ufo_projectile_time = 0
                        last_ufo_time = 0

                        ship = Ship()
                        ufo = UFO()

                        projectiles = []
                        asteroids_sets = [[], [], []]
                        ufo_projectiles = []

                        points = 0
                        main()
                    elif QUIT_BUTTON.is_clicked(mouse_pos):
                        CLICK_EFFECT.play()
                        pygame.quit()
                        sys.exit()

    pygame.quit()


def read_high_score():
    if os.path.exists("data/high_score.txt"):
        with open("data/high_score.txt", "r") as file:
            try:
                high_score = int(file.read())
            except ValueError:
                high_score = 0
    else:
        high_score = 0
    return high_score


def write_high_score(high_score):
    NEW_HIGH_SCORE_EFFECT.play()
    with open("data/high_score.txt", "w") as file:
        file.write(str(high_score))


def draw_start_menu(high_score):
    WIN.blit(BG, (0, 0))

    title_font = pygame.font.SysFont('Arial', 50)
    title_text = title_font.render("Space Boulders", 1, WHITE)
    WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 100))

    START_BUTTON.draw(WIN)

    high_score_text = HIGH_SCORE_FONT.render(f"High Score: {high_score:,}", 1, WHITE)
    WIN.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, 250))

    pygame.display.update()


def draw_game_over_screen(high_score, points):
    WIN.blit(BG, (0, 0))

    game_over_text = SCORE_FONT.render("Game Over", 1, WHITE)
    WIN.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, 100))

    score_text = SCORE_FONT.render(f"Final Score: {points:,}", 1, WHITE)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 200))
    high_score_text = HIGH_SCORE_FONT.render(f"High Score: {high_score:,}", 1, WHITE)
    WIN.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, 250))

    REPLAY_BUTTON.draw(WIN)
    QUIT_BUTTON.draw(WIN)

    pygame.display.update()


def check_for_quit_event_and_continue():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def create_new_asteroid(transfer_data, previous_asteroid_rect, projectile_angle, asteroid_rotation_change):
    return Asteroid(transfer_data, previous_asteroid_rect, projectile_angle, asteroid_rotation_change)


def handle_ufo(data):
    current_time = pygame.time.get_ticks()
    if data.ufo is None:
        if current_time - data.last_ufo_time >= UFO_COOLDOWN:
            last_ufo_time = current_time
            return UfoUpdateDataModel(UFO(), last_ufo_time)
        else:
            return UfoUpdateDataModel(data.ufo, data.last_ufo_time)
    else:  # ufo is not None
        updated_ufo = data.ufo.move_ufo()
        return UfoUpdateDataModel(updated_ufo, data.last_ufo_time)


def shoot_ufo_projectile(ufo, projectiles):
    updated_projectiles = projectiles
    if ufo is None:
        return projectiles
    else:
        updated_projectiles.append(ufo.UFOProjectile(ufo))
        return updated_projectiles


def check_which_key_pressed(data):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        data.ship.ship_angle += SHIP_ROTATION_VEL
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        data.ship.ship_angle -= SHIP_ROTATION_VEL
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        data.ship.is_accelerating = True
        data.ship.ship_rect = data.ship.move_ship()

    else:
        data.ship.is_accelerating = False
        data.ship.ship_rect = data.ship.move_ship()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if current_time - data.last_hyper_space_time >= HYPER_SPACE_COOLDOWN:
            data.ship.ship_rect.x = random.randint(0, WIDTH - data.ship.ship_rect.width)
            data.ship.ship_rect.y = random.randint(0, HEIGHT - data.ship.ship_rect.height)
            data.last_hyper_space_time = current_time
    if keys[pygame.K_SPACE]:
        if current_time - data.last_projectile_time >= PROJECTILE_COOLDOWN:
            LASER_SHOOT_EFFECT.play()
            data.last_projectile_time = current_time
            data.projectiles.append(Projectile(data.ship.ship_rect, data.ship.ship_angle))

    return data


def move_all_projectiles(projectiles, ufo_projectiles):
    updated_projectiles = []
    updated_ufo_projectiles = []
    for projectile in projectiles:
        updated_projectile_rect = projectile.move_projectile()
        if projectile.traveled_distance < HEIGHT:
            updated_projectiles.append(updated_projectile_rect)
    if ufo_projectiles is not None:
        for ufo_projectile in ufo_projectiles:
            updated_ufo_projectile_rect = ufo_projectile.move_projectile()
            if ufo_projectile.traveled_distance < HEIGHT:
                updated_ufo_projectiles.append(updated_ufo_projectile_rect)
    return updated_projectiles, updated_ufo_projectiles


def move_all_asteroids(asteroid_sets):
    updated_asteroid_sets = []
    for asteroid_set in asteroid_sets:
        updated_asteroid_set = []
        for asteroid in asteroid_set:
            new_asteroid = asteroid.move_asteroid()
            updated_asteroid_set.append(new_asteroid)
        updated_asteroid_sets.append(updated_asteroid_set)
    return updated_asteroid_sets


def check_for_projectile_collisions(projectiles, asteroid_sets, ufo, points):
    if not projectiles:
        return projectiles, asteroid_sets, ufo, points

    updated_projectiles = []
    updated_asteroid_sets = [[], [], []]
    updated_ufo = ufo
    new_points = points

    for projectile in projectiles:
        projectile_rect = projectile.projectile_rect
        projectile_alive = True
        for i, asteroid_set in enumerate(asteroid_sets):
            if not asteroid_set:
                continue
            for asteroid in asteroid_set:
                asteroid_rect = asteroid.asteroid_rect
                if asteroid not in updated_asteroid_sets[i]:
                    updated_asteroid_sets[i].append(asteroid)
                if projectile_rect.colliderect(asteroid_rect):
                    HIT_EFFECT.play()
                    projectile_alive = False
                    new_points += asteroid.point_value
                    updated_asteroid_sets[i].remove(asteroid)
                    if i < 2:
                        for new_asteroid in create_asteroid_split(i, asteroid_rect, projectile.projectile_angle):
                            updated_asteroid_sets[i + 1].append(new_asteroid)
                    break
        if ufo is not None:
            if projectile_rect.colliderect(ufo.ufo_rect):
                HIT_EFFECT.play()
                updated_ufo = None
                projectile_alive = False
                new_points += ufo.point_value
        if projectile_alive:
            updated_projectiles.append(projectile)

    return updated_projectiles, updated_asteroid_sets, updated_ufo, new_points


def create_asteroid_split(asteroid_num, previous_asteroid_rect, projectile_angle):
    new_asteroids = []
    for asteroid_rotation_change in [90, -90]:
        if asteroid_num == 0:
            new_asteroids.append(
                Asteroid(TRANSFER_DATA_ASTEROID_2, previous_asteroid_rect, projectile_angle, asteroid_rotation_change))
        elif asteroid_num == 1:
            new_asteroids.append(
                Asteroid(TRANSFER_DATA_ASTEROID_3, previous_asteroid_rect, projectile_angle, asteroid_rotation_change))
    return new_asteroids


def check_for_ship_collisions(data):
    for i, asteroid_set in enumerate(data.asteroids_sets):
        for asteroid in asteroid_set:
            if asteroid.asteroid_rect.colliderect(data.ship.ship_rect):
                data.asteroids_sets[i].remove(asteroid)
                return ShipsCollisionsDataModel(True, data.asteroids_sets, data.ufo_projectiles)
    for ufo_projectile in data.ufo_projectiles:
        if ufo_projectile.projectile_rect.colliderect(data.ship.ship_rect):
            return ShipsCollisionsDataModel(True, data.asteroids_sets, data.ufo_projectiles.remove(ufo_projectile))
    return ShipsCollisionsDataModel(False, data.asteroids_sets, data.ufo_projectiles)


def update_high_score(points, high_score):
    if points > high_score:
        high_score = points
        write_high_score(high_score)
    return high_score


def draw(ship, ship_rect, projectiles, lives, asteroid_sets, ufo, ufo_projectiles, points, high_score):
    WIN.blit(BG, (0, 0))

    for asteroid_set in asteroid_sets:
        for asteroid in asteroid_set:
            WIN.blit(asteroid.asteroid, asteroid.asteroid_rect)

    if ufo is not None:
        WIN.blit(ufo.ufo, ufo.ufo_rect)

    for ufo_projectile in ufo_projectiles:
        pygame.draw.circle(WIN, GREEN, ufo_projectile.projectile_rect.center, PROJECTILE_RADIUS)

    for projectile in projectiles:
        pygame.draw.circle(WIN, RED, projectile.projectile_rect.center, PROJECTILE_RADIUS)

    WIN.blit(ship, ship_rect)

    for live in lives:
        WIN.blit(live.live, live.live_rect)

    score_text = SCORE_FONT.render(f"Score: {points:,}", 1, "white")
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 20))
    high_score_text = HIGH_SCORE_FONT.render(f"High Score: {high_score:,}", 1, "white")
    WIN.blit(high_score_text, (WIDTH / 4 - score_text.get_width() / 2, 20))

    pygame.display.update()


if __name__ == "__main__":
    main()
