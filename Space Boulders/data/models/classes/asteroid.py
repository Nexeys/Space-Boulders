import pygame
import random
import math


class Asteroid:
    def __init__(self, data, previous_asteroid_rect, projectile_angle, asteroid_rotation_change):
        self.base_vel = data.base_vel
        self.point_value = data.point_value
        self.asteroid = pygame.image.load(data.asteroid_image)
        self.asteroid = pygame.transform.scale(self.asteroid, self.set_asteroid_size(data.size))
        self.asteroid_rect = self.asteroid.get_rect()

        if data.asteroid_number == 1:
            self.asteroid_angle = random.randint(-360, 360)
            self.asteroid_x_vel = self.base_vel * math.sin(math.radians(self.asteroid_angle)) * -1
            self.asteroid_y_vel = self.base_vel * math.cos(math.radians(self.asteroid_angle)) * -1
            asteroid_x, asteroid_y = self.set_asteroid_position()
        else:
            self.asteroid_angle = projectile_angle + asteroid_rotation_change
            self.asteroid_x_vel = self.base_vel * math.sin(math.radians(self.asteroid_angle)) * -1
            self.asteroid_y_vel = self.base_vel * math.cos(math.radians(self.asteroid_angle)) * -1
            asteroid_x = previous_asteroid_rect.centerx + self.asteroid_x_vel * 3 - self.asteroid_rect.width
            asteroid_y = previous_asteroid_rect.centery + self.asteroid_y_vel * 3 - self.asteroid_rect.height
        self.asteroid_rect = self.asteroid.get_rect(center=(asteroid_x, asteroid_y))
        self.asteroid = pygame.transform.rotate(self.asteroid, self.asteroid_angle)

    def set_asteroid_size(self, size):
        max_asteroid_width, max_asteroid_height = size
        aspect_ratio = self.asteroid.get_width() / self.asteroid.get_height()

        if aspect_ratio > 1:
            new_width = max_asteroid_width
            new_height = int(max_asteroid_width / aspect_ratio)
        else:
            new_height = max_asteroid_height
            new_width = int(max_asteroid_height * aspect_ratio)

        return new_width, new_height

    def set_asteroid_position(self):
        width, height = 800, 600
        max_distance_from_border_asteroid_spawning = 100
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            asteroid_y = random.randint(0, max_distance_from_border_asteroid_spawning)
            asteroid_x = random.randint(0, width)
        elif side == "bottom":
            asteroid_y = random.randint(height - max_distance_from_border_asteroid_spawning,
                                        height - self.asteroid_rect.height)
            asteroid_x = random.randint(0, width)
        elif side == "left":
            asteroid_x = random.randint(0, max_distance_from_border_asteroid_spawning)
            asteroid_y = random.randint(0, height)
        else:  # side == "right"
            asteroid_x = random.randint(width - max_distance_from_border_asteroid_spawning,
                                        width - self.asteroid_rect.width)
            asteroid_y = random.randint(0, height)

        return asteroid_x, asteroid_y

    def move_asteroid(self):
        width, height = 800, 600
        if self.asteroid_rect.right < 0:
            self.asteroid_rect.left = width
        elif self.asteroid_rect.left > width:
            self.asteroid_rect.right = 0
        if self.asteroid_rect.bottom < 0:
            self.asteroid_rect.top = height
        elif self.asteroid_rect.top > height:
            self.asteroid_rect.bottom = 0
        self.asteroid_rect.x += self.asteroid_x_vel
        self.asteroid_rect.y += self.asteroid_y_vel
        return self
