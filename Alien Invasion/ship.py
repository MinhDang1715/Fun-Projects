import pygame

class Ship():
    def __init__(self, screen, aiSettings):
        self.aiSettings = aiSettings

        # set the ship at the screen position
        self.screen = screen

        # load the ship image
        self.image = pygame.image.load('pic\ship.gif')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False

        # start a new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitMe(self):
        # draw the ship at it current location
        self.screen.blit(self.image, self.rect)

    def update(self, screen):
        if self.movingRight:
            # move the ship right
            if self.rect.centerx < screen.get_width() - 35:
                self.rect.centerx += self.aiSettings.shipSpeed
        if self.movingLeft:
            # move the ship left
            if self.rect.centerx > 30:
                self.rect.centerx -= self.aiSettings.shipSpeed
        if self.movingUp:
            # move the ship up
            if self.rect.centery > 70:
                self.rect.centery -= self.aiSettings.shipSpeed
        if self.movingDown:
             # move the ship down
            if self.rect.centery < screen.get_height() - 50:
                self.rect.centery += self.aiSettings.shipSpeed

    def centerShip(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def reset(self):
        # Movement flag
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False
        # start a new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
