import pygame
import random
from pygame.locals import *
from pygame.time import delay

pygame.init()

# Game Variables

run = True
CLOCK = pygame.time.Clock()
ticRate = 60

WIDTH, HEIGHT = 800, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

class GameText:
    def __init__(self):
        #font settings
        self.BLACK = [0,0,0]
        self.RED = [255,0,0]
        self.GREEN = [0,255,0]
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        # score_text
        self.score = 0
        self.textScore = self.font.render(str(self.score), True, self.GREEN, self.BLACK)
        self.textRectScore = self.textScore.get_rect()
        self.textRectScore.x = 40
        self.textRectScore.y = 50
        # gameOver_text
        self.textGameOver = self.font.render('GAME OVER', True, self.RED, self.BLACK)
        self.textRectGameOver = self.textGameOver.get_rect()
        self.textRectGameOver.x = 400
        self.textRectGameOver.y = 350

    def update(self):
        self.textScore = self.font.render(str(self.score), True, self.GREEN, self.BLACK)


class SpaceShip1:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load("SpaceShip1.png"), (100, 100))
        self.rect = self.img.get_rect()
        self.rect.y = 550
        self.health = 75
        self.bullet_list1 = []
        self.color = (0, 255, 0)
        self.bulletCD = 10
        self.bulletFired = 0
        self.hitCounter = 0
        self.onScreenBullets = 4

    def update(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[K_d]:
            self.rect.x += 10

        if self.keys[K_a]:
            self.rect.x -= 10

        if self.rect.x > 750:
            self.rect.x = 0

        if self.rect.x < 0:
            self.rect.x = 750

# bullet list 1 stuff
#practice
        self.bulletFired += 1
        if self.keys[K_SPACE]:
            if self.bulletFired > self.bulletCD:
                if len(self.bullet_list1) < self.onScreenBullets:
                    self.bullet_list1.append([self.rect.x + 48, self.rect.y])
                    self.bulletFired = 0
#


#Working Code
#        if self.keys[K_SPACE]:
    #          if len(self.bullet_list1) < 4:
 #               self.bullet_list1.append([self.rect.x + 48, self.rect.y])
#

        for i in self.bullet_list1:
            i[1] -= 10
            if i[1] < 0:
                self.bullet_list1.remove(i)

            if pygame.Rect.colliderect(pygame.Rect(i[0], i[1], 5, 10), spaceShip2.rect):
                print('hit')
                self.bullet_list1.remove(i)
                gameText.score += 250
                self.hitCounter += 1


# update healthbar colors
        if self.health > 50:
            self.color = (0, 255, 0)

        if 25 < self.health < 51:
            self.color = (255, 255, 0)

        if self.health < 26:
            self.color = (255, 0, 0)



    def render(self):
        pygame.draw.rect(WINDOW, self.color,
                         pygame.Rect(self.rect.x - 10, self.rect.y + 15, 10, self.health))

        WINDOW.blit(self.img, self.rect)
        for i in self.bullet_list1:
            pygame.draw.rect(WINDOW, (0, 20, 168), pygame.Rect(i[0], i[1], 5, 10))

class SpaceShip2:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load("SpaceShip2.png"), (100, 100))
        self.rect = self.img.get_rect()
        self.rect.y = 25
        self.rect.x = 350
        self.target = random.randint(50, 750)
        self.last_time = pygame.time.get_ticks()
        self.direction = ""
        self.bullet_list2 = []
        self.delay = random.randint(1000, 1500)
        self.last_time = pygame.time.get_ticks()

    def update(self):
        if self.target == self.rect.x:
            self.target = random.randint(50, 750)
            self.direction = ""
        else:
            if self.target > self.rect.x:
                self.direction = "RIGHT"
            else:
                self.direction = "LEFT"

        if self.direction == "RIGHT":
            self.rect.x += random.randint(5, 20)

        if self.direction == "LEFT":
            self.rect.x -= random.randint(5, 20)

#bullet list 2 stuff:

        if pygame.time.get_ticks() - self.last_time > self.delay:
            self.bullet_list2.append([self.rect.x + 48, self.rect.y + 80])
            self.last_time = pygame.time.get_ticks()
            self.delay = random.randint(1000, 1500)

        for i in self.bullet_list2:
            i[1] += 15

            if pygame.Rect.colliderect(pygame.Rect(i[0], i[1], 5, 10), spaceShip1.rect):
                print('hit')

                self.bullet_list2.remove(i)
                spaceShip1.health -= 25

    def render(self):
        WINDOW.blit(self.img, self.rect)
        for i in self.bullet_list2:
            pygame.draw.rect(WINDOW, (0, 20, 168), pygame.Rect(i[0], i[1], 5, 10))




spaceShip1 = SpaceShip1()
spaceShip2 = SpaceShip2()
gameText = GameText()

while run:
    CLOCK.tick(ticRate)
    WINDOW.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if spaceShip1.health < 5:
            pygame.QUIT
            run = False
            pygame.time.wait(500)
            pygame.quit()

    if spaceShip1.hitCounter == 4:
        ticRate = ticRate * 1.5
        spaceShip1.hitCounter = 0
        spaceShip1.bulletCD = spaceShip1.bulletCD * 1.1
        spaceShip1.onScreenBullets / 2


    if spaceShip1.health < 5:
        WINDOW.blit(gameText.textGameOver, gameText.textRectGameOver)


    gameText.update()
    WINDOW.blit(gameText.textScore, gameText.textRectScore)

    spaceShip1.update()
    spaceShip1.render()

    spaceShip2.update()
    spaceShip2.render()

    pygame.display.update()

    gameText.textRectGameOver.x = 400
    gameText.textRectGameOver.y = 350
