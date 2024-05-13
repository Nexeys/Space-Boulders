import pygame
import random
import math


class UFO:
    def __init__(self):
        width, height = 800, 600

        self.ufo = pygame.image.load("data/assets/sprites/ufo.png")
        self.ufo = pygame.transform.scale(self.ufo, self.set_ufo_size())
        self.point_value = 100
        ufo_x = random.choice((0, width - self.ufo.get_width()))
        ufo_y = random.randint(0, height - self.ufo.get_height())
        if ufo_x == 0:
            self.vel = 3
        else:
            self.vel = -3
        self.ufo_rect = self.ufo.get_rect(center=(ufo_x, ufo_y))

    def set_ufo_size(self):
        max_ship_width, max_ship_height = 50, 50
        aspect_ratio = self.ufo.get_width() / self.ufo.get_height()

        if aspect_ratio > 1:
            new_width = max_ship_width
            new_height = int(max_ship_width / aspect_ratio)
        else:
            new_height = max_ship_height
            new_width = int(max_ship_height * aspect_ratio)

        return new_width, new_height

    def move_ufo(self):
        width, height = 800, 600
        self.ufo_rect.x += self.vel
        if self.ufo_rect.right < 0:
            self.ufo_rect.left = width
        elif self.ufo_rect.left > width:
            self.ufo_rect.right = 0
        if self.ufo_rect.bottom < 0:
            self.ufo_rect.top = height
        elif self.ufo_rect.top > height:
            self.ufo_rect.bottom = 0
        return self

    class UFOProjectile:
        def __init__(self, ufo):
            self.projectile_base_vel = 12
            projectile_radius = 5
            self.projectile_angle = random.randint(-360, 360)

            self.projectile_x_vel = self.projectile_base_vel * math.sin(math.radians(self.projectile_angle)) * -1
            self.projectile_y_vel = self.projectile_base_vel * math.cos(math.radians(self.projectile_angle)) * -1
            self.projectile_x = ufo.ufo_rect.centerx + self.projectile_x_vel * 3 - projectile_radius / 2
            self.projectile_y = ufo.ufo_rect.centery + self.projectile_y_vel * 3 - projectile_radius / 2
            self.projectile_rect = pygame.Rect(self.projectile_x, self.projectile_y, projectile_radius * 2,
                                               projectile_radius * 2)
            self.traveled_distance = 0

        def move_projectile(self):
            width, height = 800, 600
            self.projectile_rect.x += self.projectile_x_vel
            self.projectile_rect.y += self.projectile_y_vel
            self.traveled_distance += self.projectile_base_vel
            if self.projectile_rect.right < 0:
                self.projectile_rect.left = width
            elif self.projectile_rect.left > width:
                self.projectile_rect.right = 0
            if self.projectile_rect.bottom < 0:
                self.projectile_rect.top = height
            elif self.projectile_rect.top > height:
                self.projectile_rect.bottom = 0
            return self
