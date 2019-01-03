import pygame

class Dead():
    def __init__(self, screen, alien):
        self.screen = screen

        # load the ship image
        self.image = pygame.image.load('pic\dead.gif')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #create an explosion rect at the center of the ship
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top
    
    def drawDead(self):
        self.screen.blit(self.image, self.rect)