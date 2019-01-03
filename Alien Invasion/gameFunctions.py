import sys
import pygame
from bullet import Bullet
from alien import Alien
from explode import Explode
from dead import Dead
from time import sleep

def checkEvents(aiSettings, screen, ship, bullet, shootSound, stats):
    keyState = pygame.key.get_pressed()
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit()
        elif events.type == pygame.KEYDOWN:
            checkKeyDown(events, ship, aiSettings, screen, bullet, shootSound, stats)
        elif events.type == pygame.KEYUP:
            checkKeyUp(events, ship)

def updateScreen(screen, ship, background, bullets, aliens, sb):
    # redraw the screen
    screen.blit(background.image, background.rect)
    # draw ship
    ship.blitMe()
    # draw scoreboard
    sb.prepScore()
    sb.showScore()
    sb.prepLive()
    sb.showLive()
    sb.prepHScore()
    sb.showHScore()
    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.drawBullet()
    # draw alien
    aliens.draw(screen)
    # make the most recently drawn screen visible
    pygame.display.flip()

def updateBullet(aiSettings, screen, ship, bullets, aliens, explosionSound, wowSound, stats, sb):
    bullets.update()
    # get rid of the unused bullet
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # check for collision with bullet
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    for hit in collision:
        explosionSound.play()
        dead = Dead(screen, hit)
        dead.drawDead()
        stats.score += 10
        sb.prepScore()
        pygame.display.flip()

    # create new fleet when we finish destroy every alien
    if len(aliens) == 0:
        bullets.empty()
        wowSound.play()
        createFleet(aiSettings, screen, ship, aliens)
        aiSettings.scaleSpeed()

    # update high score if we make a new one
    hScore = 0
    # get the high score from the file
    with open('highscore.txt') as fileObject:
        hScore = fileObject.read()
    # save high score
    if stats.score > int(hScore):
        # rewrite the high score
        with open('highscore.txt', 'w') as fileObject:
            fileObject.write(str(stats.score))
        sb.prepHScore()


def updateAlien(aiSettings, aliens, ship, failSound, stats, screen, bullets, sb):
    # check if the fleet is at an edge and then update its postion
    checkFleetEdges(aiSettings, aliens)
    aliens.update()

    # loof for alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        failSound.play()
        shipHit(aiSettings, stats, screen, ship, aliens, bullets, sb)

    # look for when an alien at the bottom of the screen
    checkAliensBottom(aiSettings, stats, screen, ship, aliens, bullets, sb, failSound)

def checkFleetEdges(aiSettings, aliens):
    for alien in aliens.sprites():
        if alien.checkEdge():
            changeFleetDirection(aiSettings, aliens)
            break

def changeFleetDirection(aiSettings, aliens):
    # drop the entire fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += aiSettings.dropSpeed
    aiSettings.fleetDirection *= -1

def fireBullet(aiSettings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group.
    newBullet = Bullet(aiSettings, screen, ship)
    bullets.add(newBullet)

def checkKeyDown(events, ship, aiSettings, screen, bullet, shootSound, stats):
    if events.key == pygame.K_RIGHT:
        ship.movingRight = True
    if events.key == pygame.K_LEFT:
        ship.movingLeft = True
    if events.key == pygame.K_UP:
        ship.movingUp = True
    if events.key == pygame.K_DOWN:
        ship.movingDown = True
    if events.key == pygame.K_SPACE:
        fireBullet(aiSettings, screen, ship, bullet)
        shootSound.play()
    if events.key == pygame.K_ESCAPE:
        hScore = 0
        # get the high score from the file
        with open('highscore.txt') as fileObject:
            hScore = fileObject.read()
        # save high score
        if stats.score > int(hScore):
            # rewrite the high score
            with open('highscore.txt', 'w') as fileObject:
                fileObject.write(str(stats.score))
        sys.exit()

def checkKeyUp(events, ship):
    if events.key == pygame.K_RIGHT:
        ship.movingRight = False
    if events.key == pygame.K_LEFT:
        ship.movingLeft = False
    if events.key == pygame.K_UP:
        ship.movingUp = False
    if events.key == pygame.K_DOWN:
        ship.movingDown = False

def getNumRow(aiSettings, shipHeight, alienHeight):
    availSpaceY = (aiSettings.screenHeight - (3 * alienHeight) - shipHeight)
    numberRows = int(availSpaceY / (3 * alienHeight))
    return numberRows

def getAlienNum(aiSettings, alienWidth):
    availSpaceX = aiSettings.screenWidth - 3 * alienWidth
    numberAlienX = int(availSpaceX / (2 * alienWidth))
    return numberAlienX

def createAlien(aiSettings, screen, aliens, alienNum, rowNum):
    alien = Alien(aiSettings, screen)
    alienWidth = alien.rect.width
    alien.x = alienWidth + 2 * alienWidth * alienNum
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * rowNum
    aliens.add(alien)

def createFleet(aiSettings, screen, ship, aliens):
    alien = Alien(aiSettings, screen)
    numberAlienX = getAlienNum(aiSettings, alien.rect.width)
    numberRow = getNumRow(aiSettings, ship.rect.height, alien.rect.height)
    for rowNum in range(numberRow):
        for alienNum in range(numberAlienX):
            createAlien(aiSettings, screen, aliens, alienNum, rowNum)

def shipHit(aiSettings, stats, screen, ship, aliens, bullets, sb):
    if stats.shipLives == 0:
        stats.gameActive = False
    else:
        # update live
        stats.shipLives -= 1
        sb.prepLive()

        explode = Explode(screen, ship)
        explode.drawExplosion()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet
        createFleet(aiSettings, screen, ship, aliens)
        ship.centerShip()
        pygame.display.flip()

        # Pause
        sleep(1)

def checkAliensBottom(aiSettings, stats, screen, ship, aliens, bullets, sb, failSound):
    screenRect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screenRect.bottom:
            failSound.play()
            # Treat this the same as if the ship got hit.
            shipHit(aiSettings, stats, screen, ship, aliens, bullets, sb)
            break

def checkStart(screen, aiSettings, stats):
    for events in pygame.event.get():
        if events.type == pygame.KEYDOWN:
            stats.gameActive = True
        if events.type == pygame.QUIT:
            sys.exit()
        
def updateStartScreen(screen, aiSettings):
    # initialize font
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 64)
    # text 1
    textSurface = myFont.render('Alien Invasion by Minh Dang', True, (255, 255, 255))
    width = textSurface.get_rect().width
    height = textSurface.get_rect().height
    # text 2
    textSurface2 = myFont.render('Press any key to play', True, (255, 255, 255))
    width2 = textSurface2.get_rect().width
    height2 = textSurface2.get_rect().height
    screen.blit(textSurface, ((aiSettings.screenWidth - width) / 2, 
                                (aiSettings.screenHeight - height) / 2  - 100))
    screen.blit(textSurface2, ((aiSettings.screenWidth - width2) / 2, 
                                (aiSettings.screenHeight - height2) / 2))
    # make the most recently drawn screen visible
    pygame.display.flip()

def checkEnd(screen, aiSettings, stats):
    for events in pygame.event.get():
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_ESCAPE:
                sys.exit()
            if events.key == pygame.K_r:
                stats.gameActive = True
        if events.type == pygame.QUIT:
            sys.exit()

def updateEndScreen(screen, aiSettings):
    # initialize font
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 64)
    textSurface = myFont.render('Game Over', True, (255, 255, 255))
    textSurface2 = myFont.render('Press R to try again or Esc to Quit', True, (255, 255, 255))
    textSurface3 = myFont.render('Thank you for playing', True, (255, 255, 255))
    width1 = textSurface.get_rect().width
    height1 = textSurface.get_rect().height
    width2 = textSurface2.get_rect().width
    height2 = textSurface2.get_rect().height
    width3 = textSurface3.get_rect().width
    height3 = textSurface3.get_rect().height
    screen.fill((0, 0, 0))
    screen.blit(textSurface, ((aiSettings.screenWidth - width1) / 2, 
                                (aiSettings.screenHeight - height1) / 2 - 100))
    screen.blit(textSurface2, ((aiSettings.screenWidth - width2) / 2, 
                                (aiSettings.screenHeight - height2) / 2))
    screen.blit(textSurface3, ((aiSettings.screenWidth - width3) / 2, 
                                (aiSettings.screenHeight - height3) / 2 + 100))
    # make the most recently drawn screen visible
    pygame.display.flip()