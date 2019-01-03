import pygame

class Explode():
    def __init__(self, screen, ship):
        self.screen = screen

        # load the ship image
        self.image = pygame.image.load('pic\explode.gif')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #create an explosion rect at the center of the ship
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
    
    def drawExplosion(self):
        self.screen.blit(self.image, self.rect)
            