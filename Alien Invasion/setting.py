class Setting():
    def __init__(self):
        # general setting
        self.screenWidth = 1280
        self.screenHeight = 720
        self.caption = 'Alien Invasion'

        # ship setting
        self.shipSpeed = 7
        self.shipLives = 3

        # bullet setting
        self.bulletSpeed = 7
        self.bulletDelay = 1

        # alien setting
        self.alienSpeed = 5
        self.dropSpeed = 15
        # 1 = right, -1 = left
        self.fleetDirection = 1

        # sound
        self.pew = 'sound/pew.wav'
        self.boom = 'sound/boom.wav'
        self.wow = 'sound/wow.wav'
        self.fail = 'sound/fail.wav'
        self.background = 'sound/background.wav'

        # explosion
        self.explosion = 'pic/explode.gif'

        # speed up after next level
        self.speedUp = 1.1

        self.scaleSpeed()
    
    def scaleSpeed(self):
        self.shipSpeed *= self.speedUp
        self.bulletSpeed *= self.speedUp
        self.alienSpeed *= self.speedUp
    
    def reset(self):
        self.shipSpeed = 7
        self.bulletSpeed = 7
        self.alienSpeed = 5