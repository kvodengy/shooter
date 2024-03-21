import pygame
from random import randint
pygame.font.init()
pygame.mixer.init()

FPS = pygame.time.Clock()
win_width = 1280
win_height = 665
p_size = 100

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

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x<win_width-self.rect.width:
            self.rect.x += self.speed 
    def crash(self, l):
        for w in l:
            if self.rect.colliderect(w.rect):
                return True
            else:
                return False
            
class Enemy(Player):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)
        self.direction = True #right

    def move(self, amount):
        i = 0
        self.rect.y += self.speed
        if self.rect.y>670:
            self.rect.x = randint(0,win_width)
            self.rect.y = -20
            i = i + 1

    #def move2(self):
        #self.rect.y += self.speed



bg = Settings("background.png", 0, 0, win_width, win_height)
player = Player("rocket.png", win_width//2.05, win_height//1.25, p_size, p_size, 10)
enemy = Enemy("alien.png", randint(0,win_width), 0, p_size, p_size, 10)
#boss = Enemy("alien.png", randint(0,win_width), 0, p_size*2, p_size*2, 5)

game = True
i = 1


pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.play()

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    bg.draw()
    player.draw()
    player.move()
    enemy.draw()
    enemy.move(3)
    #boss.draw()
    #boss.move2()

    pygame.display.flip()
    FPS.tick(60)