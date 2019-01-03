import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, aiSettings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.aiSettings = aiSettings

        # load the image
        self.image = pygame.image.load('pic/ufo.gif')
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def checkEdge(self):
        screenRect = self.screen.get_rect()
        if self.rect.right >= screenRect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        # move the alien right or left
        self.x += (self.aiSettings.alienSpeed * self.aiSettings.fleetDirection)
        self.rect.x = self.x

    def blitMe(self):
        self.screen.blit(self.image, self.rect)