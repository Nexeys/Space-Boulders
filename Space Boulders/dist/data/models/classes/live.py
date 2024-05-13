import pygame


class Live:
    def __init__(self, location):
        self.live = pygame.image.load('data/assets/sprites/Live.png')
        self.live = pygame.transform.scale(self.live, self.set_live_size())
        self.live_rect = self.live.get_rect(center=location)

    def set_live_size(self):
        max_live_width, max_live_height = 40, 40
        aspect_ratio = self.live.get_width() / self.live.get_height()

        if aspect_ratio > 1:
            new_width = max_live_width
            new_height = int(max_live_width / aspect_ratio)
        else:
            new_height = max_live_height
            new_width = int(max_live_height * aspect_ratio)

        return new_width, new_height
