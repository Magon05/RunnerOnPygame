import pygame
from pygame.locals import *
import time, random, sqlite3, datetime

pygame.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("CatRunner")
FPS = pygame.time.Clock()
background = pygame.image.load("background.jpg")
score = 0
font = pygame.font.SysFont("arial", 25, False, True)
reload = 0
speed = 10

def menu():
    screen.blit(background, (0, 0))
    run_game = True
    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run_game = False
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        newgame_text = font.render("New game", True, (0, 0, 0))
        score_text = font.render("Score", True, (0, 0, 0))
        screen.blit(newgame_text, (600, 400))
        screen.blit(score_text, (600, 450))
        if 700 > mouse[0] > 600 and 425 > mouse[1] > 400:
            if click == (1, 0, 0):
                game_loop()
        elif 700 > mouse[0] > 600 and 475 > mouse[1] > 450:
            if click == (1, 0, 0):
                show_record()
        pygame.display.update()

def show_record():
    text = open("records.txt", "r")
    inform_text = text.read()
    text.close()
    screen_level_score = font.render('Score :' + inform_text, True, (0,0,0))
    screen.blit(screen_level_score, (100, 100))
    pygame.display.update()

class Hero(pygame.sprite.Sprite):
    imagelist = ["herorun1.png", "herorun2.png", "herorun3.png", "herorun4.png", "herorun5.png", "herorun6.png",
                 "herorun7.png", "herorun8.png"]
    image = pygame.image.load("herorun1.png")
    rect = image.get_rect(center=(100, 800))

    def animation(self, animpoint):
        self.image = pygame.image.load(self.imagelist[animpoint])
        screen.blit(self.image, self.rect)

    def jump(self):
        self.image = pygame.image.load("herojump.png")
        if self.rect.top > 400:
            self.rect.move_ip(0, -60)

        screen.blit(self.image, self.rect)

    def gravitattion(self):
        if self.rect.top < 700:
            self.image = pygame.image.load("herofall.png")
            self.rect.move_ip(0, 15)

class Rock(pygame.sprite.Sprite):
    image = pygame.image.load("rock.png")
    rect = image.get_rect(center=(1200, 840))

    def draw(self):
        global score, reload
        self.x = random.randrange(1200, 1400)
        if self.rect.right < 0:
            score += 1
            self.rect = self.image.get_rect(center=(self.x, 840))
        elif reload == 1:
            score = 0
            self.rect.left = self.x
        else:
            screen.blit(self.image, self.rect)
            self.rect.move_ip(-25, 0)

class Tree(pygame.sprite.Sprite):
    image = pygame.image.load("tree.png")
    rect = image.get_rect(center=(2500, 800))

    def draw(self):
        global score, reload
        self.x = random.randrange(2500, 3000)
        if self.rect.right < 0:
            score += 1
            self.rect = self.image.get_rect(center=(self.x, 800))
        elif reload == 1:
            score = 0
            self.rect.left = self.x
        else:
            screen.blit(self.image, self.rect)
            self.rect.move_ip(-30, 0)

class Bee(pygame.sprite.Sprite):
    image = pygame.image.load("bee.png")
    rect = image.get_rect(center=(1800, 400))
    anim = 0

    def draw(self):
        global score, reload
        self.x = random.randrange(1600, 1800)
        self.y = random.randrange(400, 500)
        if self.rect.right < 0:
            score += 1
            self.rect = self.image.get_rect(center=(self.x, self.y))
        elif reload == 1:
            score = 0
            self.rect.left = self.x
            self.rect.top = self.y
        else:
            screen.blit(self.image, self.rect)
            self.rect.move_ip(-30, 0)

H1 = Hero()
R1 = Rock()
B1 = Bee()
T1 = Tree()
enemies = pygame.sprite.Group()
enemies.add(R1, B1, T1)

def game_loop():
    screen.blit(background, (0, 0))
    pygame.mixer.music.load('Happy walk.mp3')
    pygame.mixer.music.play()
    animpoint = 0

    run_game = True
    global score, speed, reload

    while run_game:
        if animpoint == 8:
            animpoint = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run_game = False

        screen.blit(background, (0, 0))
        if pygame.sprite.spritecollideany(Hero, enemies):
            sound = pygame.mixer.Sound('cartoon-throw.wav')
            sound.play()
            time.sleep(3)
            #rec_list = open('records.txt', 'w')
            #rec_list.write(f"{score_record}\n")
            #rec_list.close()
            reload = 1
            run_game = False

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            H1.jump()
            # jump_sound.play()
        else:
            H1.gravitattion()
            H1.animation(animpoint)

        if score == 10:
            speed = 15
        elif score == 20:
            speed = 20
        elif score == 30:
            speed = 25
        elif score == 40:
            speed = 30
        animpoint += 1
        R1.draw()
        B1.draw()
        #T1.draw()
        reload = 0
        score_text = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (1100, 100))
        score_record = str(score)
        pygame.display.update()
        FPS.tick(speed)

menu()
