import pygame
from sys import exit
from pygame.locals import *
from pygame import mixer 

player = []
player_pos = 0

mixer.init()
mixer.music.load('achtergrondsound.mp3')
mixer.music.set_volume(0.2)
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
        player_pos.x -= 10
    elif motion == "right" and player_pos.x < 1560:
        player_pos.x += 10



def player_show():
    pygame.draw.rect(screen, "red", rect, 1)
    

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

    player_show()
    pygame.display.update()
    clock.tick(60)
        