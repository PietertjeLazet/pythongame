import pygame
from sys import exit
from pygame.locals import *
from pygame import mixer 

player = []
player_pos = 0

bullets = []
kaagjes = []


mixer.init()
mixer.music.load('achtergrondsound.mp3')
mixer.music.set_volume(1)
mixer.music.play()

pygame.init()
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption('Pvv invaders')
clock = pygame.time.Clock()

img = pygame.image.load('player.jpg')
img.convert()
rect = img.get_rect()

bg = pygame.image.load("nederland.png")
bg = pygame.transform.scale(bg, (1600, 800))

icon = pygame.image.load("geert.jpg")

pygame.display.set_icon(icon)

shot = pygame.mixer.Sound("spugen.mp3")
enemy = pygame.mixer.Sound("wildersminderkaag.mp3")

def player_setup():
    global player_pos
    #x
    player.append(int(800))
    #y
    player.append(int(700))
    player_pos = pygame.Vector2(player[0], player[1])
    
player_setup() 



def player_move(motion):
    global player_pos
    
    if motion == "left" and player_pos.x > 0:
        player_pos.x -= 3
    elif motion == "right" and player_pos.x < 1560:
        player_pos.x += 3



def player_show():
    pygame.draw.rect(screen, "red", rect, 1)

class bullet(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 30
        self.vel = 5
        self.radius = 2
        
    def draw(self,window):
        print(str(self.x))
        pygame.draw.circle(window, "red", self.x, self.radius)
        
    
    def update():
        pass
        

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    
    rect.center = player_pos[0], player_pos[1]
    screen.blit(bg, (0,0))
    
    screen.blit(img, rect)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_move("left")
    if keys[pygame.K_d]:
        player_move("right")
    if keys[pygame.K_SPACE]:
        bullets.append(bullet((player_pos.x, player_pos.y), 1))
        print(bullets)
    if keys[pygame.K_u]:
        enemy.play()
    if keys[pygame.K_r]:
        shot.play()
        pygame.time.delay(2000)
        
    for bullet in bullets:
        bullet.draw(screen)

    player_show()
    pygame.display.update()
    clock.tick(150)

    #print(clock.get_fps())
        