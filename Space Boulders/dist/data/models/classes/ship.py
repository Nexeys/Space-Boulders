import pygame
import math


def set_ship_size(ship):
    max_ship_width, max_ship_height = 50, 50
    aspect_ratio = ship.get_width() / ship.get_height()

    if aspect_ratio > 1:
        new_width = max_ship_width
        new_height = int(max_ship_width / aspect_ratio)
    else:
        new_height = max_ship_height
        new_width = int(max_ship_height * aspect_ratio)

    return new_width, new_height


class Ship:
    def __init__(self):
        width, height = 800, 600

        self.is_accelerating = False
        self.original_ship = pygame.image.load("data/assets/sprites/Ship.png").convert_alpha()
        new_ship_size = set_ship_size(self.original_ship)
        self.original_ship = pygame.transform.scale(self.original_ship, new_ship_size)
        self.ship_angle = 0
        self.ship_rect = self.original_ship.get_rect(center=(width / 2, height / 2))
        self.ship_base_vel = 0
        self.deceleration_speed = 0.05
        self.acceleration_speed = 0.25

    def move_ship(self):
        width, height = 800, 600
        starting_deceleration_speed = 7
        max_acceleration_speed = 9
        if self.is_accelerating:
            self.acceleration_speed *= 1.005
            if self.ship_base_vel - self.acceleration_speed < max_acceleration_speed:
                self.ship_base_vel += self.acceleration_speed
            else:
                self.ship_base_vel = 9
            ship_x_vel = self.ship_base_vel * math.sin(math.radians(self.ship_angle)) * -1
            ship_y_vel = self.ship_base_vel * math.cos(math.radians(self.ship_angle)) * -1
            self.deceleration_speed = 0.05
        else:
            self.acceleration_speed = 0.25
            self.deceleration_speed *= 1.005
            if self.ship_base_vel - self.deceleration_speed > 0:
                if self.ship_base_vel > starting_deceleration_speed:
                    self.ship_base_vel = starting_deceleration_speed
                self.ship_base_vel -= self.deceleration_speed
            else:
                self.ship_base_vel = 0
            ship_x_vel = self.ship_base_vel * math.sin(math.radians(self.ship_angle)) * -1
            ship_y_vel = self.ship_base_vel * math.cos(math.radians(self.ship_angle)) * -1

        if self.ship_rect.right < 0:
            self.ship_rect.left = width
        elif self.ship_rect.left > width:
            self.ship_rect.right = 0
        if self.ship_rect.bottom < 0:
            self.ship_rect.top = height
        elif self.ship_rect.top > height:
            self.ship_rect.bottom = 0
        return self.ship_rect.move(ship_x_vel, ship_y_vel)
