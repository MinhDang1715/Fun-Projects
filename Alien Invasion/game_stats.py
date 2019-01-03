class GameStats():
    def __init__(self, aiSettings):
        self.aiSettings = aiSettings
        self.resetStats()

        # start the game in an inactive state
        self.gameActive = False

        # score
        self.score = 0

        # lives
        self.shipLives = aiSettings.shipLives

    def resetStats(self):
        self.shipLives = self.aiSettings.shipLives
        self.score = 0