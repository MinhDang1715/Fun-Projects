import pygame.font

class Scoreboard():
    def __init__(self, aiSettings, screen, stats):
        self.screen = screen
        self.screenRect = screen.get_rect()
        self.aiSettings = aiSettings
        self.stats = stats

        self.textColor = (255, 255, 255)
        self.font = pygame.font.SysFont('Comic Sans MS', 22)

        self.prepScore()
        self.prepLive()
        self.prepHScore()

    def prepScore(self):
        scoreStr = 'Score: ' + str(self.stats.score)
        self.scoreImg = self.font.render(scoreStr, True, self.textColor)

        self.scoreRect = self.scoreImg.get_rect()
        self.scoreRect.center = self.screenRect.center
        self.scoreRect.top = 10

    def showScore(self):
        self.screen.blit(self.scoreImg, self.scoreRect)

    def prepLive(self):
        liveStr = 'Lives: ' + str(self.stats.shipLives)
        
        self.liveImg = self.font.render(liveStr, True, self.textColor)

        self.liveRect = self.scoreImg.get_rect()
        self.liveRect.left = self.screenRect.left + 20
        self.liveRect.top = 10

    def showLive(self):
        self.screen.blit(self.liveImg, self.liveRect)

    # high score of the game is store in the highscore.txt file
    def prepHScore(self):
        hScore = 0
        # get the high score from the file
        with open('highscore.txt') as fileObject:
            hScore = fileObject.read()
        hScoreStr = 'High Score: ' + str(hScore)
        self.hScoreImg = self.font.render(hScoreStr, True, self.textColor)

        self.hScoreRect = self.scoreImg.get_rect()
        self.hScoreRect.right = self.screenRect.right - 100
        self.hScoreRect.top = 10

    def showHScore(self):
        self.screen.blit(self.hScoreImg, self.hScoreRect)