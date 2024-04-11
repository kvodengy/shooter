import pygame
from random import randint
import time

pygame.font.init()
pygame.mixer.init()

FPS = pygame.time.Clock()
win_width = 1280
win_height = 660
p_size = 100
enemies = []
bullets = []

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Шутер")

class Settings():
    def __init__(self, image, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Settings):
    
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h)
        self.speed = s
        self.bullets = []
        self.hp = 3
        self.image_hp = pygame.transform.scale(pygame.image.load("heart.png"), (100,100))

    def draw_hp(self):
        for h in range(self.hp):
            window.blit(self.image_hp, (h*100,0))

    def move(self):
        self.draw_hp()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x<win_width-self.rect.width:
            self.rect.x += self.speed 

    def bulletshoot(self):
        global shoot
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and shoot:
            shoot = False
            bullets.append(Bullet("bullet.png", self.rect.centerx-20, self.rect.centery//1.25, 50, 100, 20))
            
class Enemy(Player):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)

    def move(self):
        global player, enemies
        self.rect.y += self.speed
        if self.rect.colliderect(player.rect) and self in enemies:
            player.hp -= 1
            enemies.remove(self)
        if self.rect.y>win_height-p_size:
            self.rect.x = randint(0,win_width-p_size)
            self.rect.y = randint(-10*p_size, -1*p_size)
        for e in enemies:
            if e != self and self.rect.colliderect(e.rect):
                self.rect.x = randint(0,win_width-p_size)
                self.rect.y = randint(-10*p_size, -1*p_size)


def levels():
    global enemies, num_enemies, start, num_level, boss
    if start == True and num_level==1:
        num_enemies = 1
        for enemy in range(num_enemies):
            enemies.append(Enemy("alien.png", randint(0,win_width), randint(-5*p_size, -1*p_size), p_size, p_size, 5))
        start = False
        boss = Boss("boss.png", win_width//4, -400, win_width//2, 400, 5, 15)

class Bullet(Player):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)

    def move(self):
        global enemies, bullets
        self.rect.y -= self.speed
        if self.rect.y < -10:
            bullets.remove(bullet)
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and self in bullets:
                enemies.remove(enemy)
                bullets.remove(bullet)
        if self.rect.colliderect(boss.rect) and self in bullets:
                    boss.hp -= 1
                    bullets.remove(self)
    def b_shoot(self):
        global player, boss, enemies
        self.rect.y += self.speed
        if self.rect.y > win_height and self in boss.boss_bullets:
            boss.boss_bullets.remove(self)
        if self.rect.colliderect(player.rect) and self in boss.boss_bullets:
            player.hp -= 1
            boss.boss_bullets.remove(self)
        

            
class Boss(Player):
    def __init__(self, image, x, y, w, h, s, hp):
        super().__init__(image, x, y, w, h, s)
        self.start = False
        self.boss_bullets = []
        self.hp = hp
        self.hp1 = self.hp
        self.rect_hp = pygame.Rect(self.rect.x, 0, self.rect.width, 20)

    def move(self):
        self.show_hp()
        if self.rect.y<20:
            self.rect.y += self.speed
        else:
            self.start = True


    def show_hp(self):
        w = self.hp * self.rect.width/self.hp1

        self.rect_hp2 = pygame.Rect(self.rect.x, 0, w, 20)
        pygame.draw.rect(window, "red", self.rect_hp)
        pygame.draw.rect(window, "green", self.rect_hp2)

    def shootboss(self):
        if self.start == True and len(self.boss_bullets)==0:
            x=randint(320, 960)
            for i in range(randint(1,2)):
                self.boss_bullets.append(Bullet("bullet.png", x, self.rect.y+self.rect.height//2, 20, 40, 15))
                self.start = False
        elif self.start == False and len(self.boss_bullets)==0:
            self.start = True




bg = Settings("background.png", 0, 0, win_width, win_height)
player = Player("rocket.png", win_width//2.05, win_height//1.25, p_size, p_size, 20) 

finish = False
start = True
num_level = 1
game = True
current = time.time()
shoot = True


pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.play()

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    
    if finish != True:
        bg.draw()
        
        levels()

        if time.time()-current>0.5:
            current = time.time()
            shoot = True
    
        for enemy in enemies:
            enemy.move()
            enemy.draw()

        for bullet in bullets:
            bullet.move()
            bullet.draw()

        if player.hp <= 0:
            finish = True

        if len(enemies) == 0:
            boss.move()
            boss.shootboss()
            boss.draw()
            for b in boss.boss_bullets:
                b.b_shoot()
                b.draw()

        player.draw()
        player.move()
        player.bulletshoot()
    
    pygame.display.flip()
    FPS.tick(60)