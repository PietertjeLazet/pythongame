import pygame
from sys import exit
from pygame.locals import *

player = []
player_pos = 0

pygame.init()
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption('Pvv invaders')
clock = pygame.time.Clock()

bg = pygame.image.load(r"C:\Users\piete\OneDrive\Afbeeldingen\nederland.png")
bg = pygame.transform.scale(bg, (1600, 800))

def player_setup():
    global player_pos
    #x
    player.append(int(800))
    #y
    player.append(int(700))
    player_pos = pygame.Vector2(player[0], player[1])
    

def player_move(motion):
    global player_pos
    
    if motion == "left":
        player_pos.x -= 10
    elif motion == "right":
        player_pos.x += 10

player_setup()

def player_show():
    pygame.draw.circle(screen, "red", player_pos, 40)
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    
    screen.blit(bg, (0,0))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_move("left")
    if keys[pygame.K_d]:
        player_move("right")

    player_show()
    pygame.display.update()
    clock.tick(60)
        