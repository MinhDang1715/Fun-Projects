import sys
import pygame
from pygame.sprite import Group
import gameFunctions as gf
from setting import Setting
from ship import Ship
from background import Background
from game_stats import GameStats
from scoreboard import Scoreboard

def run_game():
    # intialize
    pygame.init()
    pygame.mixer.init()
    # save y of bGround to move it up
    y = 0
    bGround = Background('pic/background.png', [0, y])
    aiSettings = Setting()
    screen = pygame.display.set_mode((aiSettings.screenWidth, aiSettings.screenHeight))
    pygame.display.set_caption(aiSettings.caption)

    # create an instance to store game statistics and scoreboard
    stats = GameStats(aiSettings)
    sb = Scoreboard(aiSettings, screen, stats)

    # sound effect
    shootSound = pygame.mixer.Sound(aiSettings.pew)
    explosionSound = pygame.mixer.Sound(aiSettings.boom)
    wowSound = pygame.mixer.Sound(aiSettings.wow)
    failSound = pygame.mixer.Sound(aiSettings.fail)

    pygame.mixer.music.load(aiSettings.background)
    pygame.mixer.music.set_volume(0.3)

    # make ship
    ship = Ship(screen, aiSettings)

    # make a group to store the bullet
    bullets = Group()

    # make an alien group
    aliens = Group()

    # make an explosion group
    explode = Group

    # play background music
    pygame.mixer.music.play(loops=-1)

    # start screen
    while True:
        gf.checkStart(screen, aiSettings, stats)
        if not stats.gameActive:
            gf.updateStartScreen(screen, aiSettings)
        else:    
            break

    # main game
    gf.createFleet(aiSettings, screen, ship, aliens)
    # start the main loop for the game
    while True:
        if stats.gameActive:
            gf.checkEvents(aiSettings, screen, ship, bullets, shootSound, stats)
            ship.update(screen)
            gf.updateBullet(aiSettings, screen, ship, bullets, aliens, explosionSound, 
                            wowSound, stats, sb)
            gf.updateAlien(aiSettings, aliens, ship, failSound, stats, screen, bullets, sb) 
            gf.updateScreen(screen, ship, bGround, bullets, aliens, sb)
        else:
            # end screen
            gf.checkEnd(screen, aiSettings, stats)
            aliens.empty()
            bullets.empty()
            if not stats.gameActive:
                gf.updateEndScreen(screen, aiSettings)
            else:
                stats.resetStats()
                aiSettings.reset()
                ship.reset()

run_game()
  