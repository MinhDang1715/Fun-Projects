import pygame

class Background():
    def __init__(self, file, location):
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

