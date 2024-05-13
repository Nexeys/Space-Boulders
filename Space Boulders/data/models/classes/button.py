import pygame


class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont('Arial', 30)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, 'black')
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
