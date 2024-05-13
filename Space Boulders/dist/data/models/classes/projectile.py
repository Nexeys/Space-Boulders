import pygame
import math


class Projectile:

    def __init__(self, ship_rect, ship_angle):
        self.projectile_base_vel = 12
        projectile_radius = 5

        self.projectile_x_vel = self.projectile_base_vel * math.sin(math.radians(ship_angle)) * -1
        self.projectile_y_vel = self.projectile_base_vel * math.cos(math.radians(ship_angle)) * -1
        self.projectile_x = ship_rect.centerx + self.projectile_x_vel * 3 - projectile_radius / 2
        self.projectile_y = ship_rect.centery + self.projectile_y_vel * 3 - projectile_radius / 2
        self.projectile_rect = pygame.Rect(self.projectile_x, self.projectile_y, projectile_radius * 2,
                                           projectile_radius * 2)
        self.projectile_angle = ship_angle
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
