import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, aiSettings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        self.image = pygame.image.load('pic/bullet.gif')
        self.rect = self.image.get_rect()

        #create a bullet rect at (0, 0) then set at the correct position
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet postion
        self.y = self.rect.y

        self.speed = aiSettings.bulletSpeed

    def drawBullet(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        #move the bullet up the screen
        self.y -= self.speed
        self.rect.y = self.y