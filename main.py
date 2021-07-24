import pygame
from pygame.locals import *
import time, random, sqlite3, datetime

pygame.init()
screen = pygame.display.set_mode((1200, 900))
FPS = pygame.time.Clock()
background = pygame.image.load("background.jpg")
score = 0
font = pygame.font.SysFont("arial", 25, False, True)  # Для работы со шрифтами
db = sqlite3.connect("record.db")#Подключаем базу данных
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS list ( 
	record TEXT
	)""")
db.commit()

def menu():
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        mouse = pygame.mouse.get_pos()  # позиция курсора мыши
        click = pygame.mouse.get_pressed()
        newgame_text = font.render("New game", True, (0, 0, 0))
        score_text = font.render("Score", True, (0, 0, 0))
        screen.blit(newgame_text, (600, 400))
        screen.blit(score_text, (600, 450))
        if 700 > mouse[0] > 600 and 425 > mouse[1] > 400:
            if click == (1, 0, 0):
                game_loop()
                break
        elif 700 > mouse[0] > 600 and 475 > mouse[1] > 450:
            if click == (1, 0, 0):
                show_record()
        pygame.display.update()

def show_record():
    for i in sql.execute("SELECT MAX(record) FROM list"):
        inform = "Max record is  " + "".join(i)
    inform_text = font.render(inform, True, (0, 0, 0))
    screen.blit(inform_text, (100, 100))
    pygame.display.update()

class Hero(pygame.sprite.Sprite):
    imagelist = ["herorun1.png", "herorun2.png", "herorun3.png", "herorun4.png", "herorun5.png", "herorun6.png", "herorun7.png", "herorun8.png"]
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

def load_sound(file):
    if not pygame.mixer:
        return None
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print("Warning, unable to load, %s" % file)
    return None

class Rock(pygame.sprite.Sprite):
    image = pygame.image.load("rock.png")
    rect = image.get_rect(center=(1200, 840))

    def draw(self):
        self.x = random.randrange(1200, 1400)
        if self.rect.right < 0:
            global score
            score += 1
            self.rect.left = self.x
        else:
            screen.blit(self.image, self.rect)
            self.rect.move_ip(-30, 0)

class Bat(pygame.sprite.Sprite):
    imagelist = ["bat1.png", "bat2.png"]
    image = pygame.image.load("bat1.png")
    rect = image.get_rect(center=(1800, 400))
    anim = 0

    def animation(self):
        if self.anim > 1:
            self.anim = 0
        self.image = pygame.image.load(self.imagelist[self.anim])
        screen.blit(self.image, self.rect)
        self.anim += 1

    def draw(self):
        self.x = random.randrange(1600, 1800)
        self.y = random.randrange(300, 400)
        if self.rect.right < 0:
            global score
            score += 1
            self.rect.left = self.x
            self.rect.top = self.y
        else:
            screen.blit(self.image, self.rect)
            self.rect.move_ip(-30, 0)

R1 = Rock()
B1 = Bat()
H1 = Hero()
enemies = pygame.sprite.Group()
enemies.add(R1, B1)

def game_loop():
    pygame.mixer.music.load('Happy walk.mp3')
    pygame.mixer.music.play()
    screen.blit(background, (0, 0))
    animpoint = 0
    speed = 10
    #jump_sound = load_sound('jump_06.wav')
    fall_sound = load_sound('cartoon-throw.wav')
    while True:
        if animpoint == 8:
            animpoint = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        screen.blit(background, (0, 0))
        if pygame.sprite.spritecollideany(Hero, enemies):
            fall_sound.play()
            time.sleep(3)
            sql.execute(f"INSERT INTO list VALUES (?)",(score_record))
            db.commit()
            menu()
            break
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            H1.jump()
            #jump_sound.play()
        else:
            H1.gravitattion()
            H1.animation(animpoint)
        global score
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
        B1.animation()
        B1.draw()
        score_text = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (1100, 100))
        score_record = str(score)
        pygame.display.update()
        FPS.tick(speed)

if __name__ == "__main__":
    menu()