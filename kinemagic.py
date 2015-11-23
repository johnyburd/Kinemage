import pygame, random, sys
from pygame.locals import *
import pygame.mixer

WINDOWWIDTH = 1022
WINDOWHEIGHT = 273
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
BACKGROUNDIMAGE = pygame.image.load("assets/background.png")
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 6
ADDNEWBADDIERATE = 20#96
PLAYERMOVERATE = 5


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)  ########## TEXT

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Kinemagic')
pygame.mouse.set_visible(False)

# set up fonts
#font = pygame.font.SysFont(None, 48)
font = pygame.font.Font("assets/freesansbold.ttf",16)

# set up sounds
gameOverSound = pygame.mixer.Sound('assets/gameover.wav')
pygame.mixer.music.load('assets/background.wav')

# set up images
playerImage = pygame.image.load('assets/player.png')
playerImagebuffer = playerImage
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('assets/duck.png')

# show the "Start" screen
drawText('Kinemagic', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = spamCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == ord('k'):
                    oldRate = ADDNEWBADDIERATE
                    spamCheat = True

                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                    playerImagebuffer = playerImage
                    playerImage = pygame.image.load('assets/playerLeft.png')

                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                    playerImagebuffer = playerImage
                    playerImage = pygame.image.load('assets/player.png')

                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                    playerImagebuffer = playerImage
                    playerImage = pygame.image.load('assets/playerTurned.png')

                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                    playerImagebuffer = playerImage
                    playerImage = pygame.image.load('assets/playerFacing.png')


            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    #score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    #score = 0
                if event.key == ord('k'):
                    spamCheat = False
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                    
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                    
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                    
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

#            if not moveUp ^ moveDown ^ moveRight ^ moveLeft:
               # playerImage = playerImagebuffer

            #if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                #playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE or spamCheat == True:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
       # windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(BACKGROUNDIMAGE, (0, 0))

        # Draw the score and top score.
        #drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        #drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)    ######  score  #####

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    #pygame.mixer.music.stop()
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('Death by Force of Duck.', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
