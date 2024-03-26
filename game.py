import pygame
from sys import exit
from pygame.locals import *
from pygame import mixer 

player = []
player_pos = 0

bullets = []
enemies = []


mixer.init()
mixer.music.load('achtergrondsound.mp3')
mixer.music.set_volume(1)
mixer.music.play()

pygame.init()
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption('Pvv invaders')
clock = pygame.time.Clock()


img = pygame.image.load('player.jpg')
img = pygame.transform.scale(img, (150, 100))

img.convert()
rect = img.get_rect()

bullet_img = pygame.image.load('kogel.jpg')
bullet_img = pygame.transform.scale(bullet_img, (20, 20))  # Adjust the size as needed

bg = pygame.image.load("nederland.png")
bg = pygame.transform.scale(bg, (1600, 800))

icon = pygame.image.load("geert.jpg")

pygame.display.set_icon(icon)

shot = pygame.mixer.Sound("spugen.mp3")
enemy = pygame.mixer.Sound("wildersminderkaag.mp3")

last_bullet_time = -1000

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
    
    if motion == "left" and player_pos.x > 75:
        player_pos.x -= 3
    elif motion == "right" and player_pos.x < 1525:
        player_pos.x += 3



def player_show():
    pygame.draw.rect(screen, "red", rect, 1)

class Bullet:
    def __init__(self, pos, vel, img):
        self.pos = pos
        self.vel = 4
        self.img = img
        self.radius = 5  # Set a fixed radius for the bullet

    def draw(self, window):
        window.blit(self.img, (int(self.pos[0]), int(self.pos[1])))

    def update(self):
        self.pos = (self.pos[0], self.pos[1] - self.vel)
        
class Enemy:
    def __init__(self, pos):
        self.pos = pos
        self.vel = 0.05
        self.width = 10
        self.height = 30
        self.radius = 20

    def draw(self, window):
        pygame.draw.circle(window, "red", tuple(map(int, self.pos)), self.radius)
        
    def update(self):
        self.pos = (self.pos[0], self.pos[1] + self.vel)


        
for j in range(4):  # Two rows
    for i in range(10):  # Ten enemies per row
        enemies.append(Enemy([40 + i*160, 30 + j*60]))  # Adjust the vertical position for each row


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
        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time >= 500:
            bullets.append(Bullet(player_pos, 1, bullet_img))
            last_bullet_time = current_time
    if keys[pygame.K_u]:
        enemy.play()
    if keys[pygame.K_r]:
        shot.play()
        pygame.time.delay(2000)
        

    
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)
    for enemy in enemies:
        enemy.update()
        enemy.draw(screen)
        
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dist = ((bullet.pos[0] - enemy.pos[0])**2 + (bullet.pos[1] - enemy.pos[1])**2)**0.5
            if dist < bullet.radius + enemy.radius:
                bullets.remove(bullet)  
                enemies.remove(enemy)
                break
        if bullet.pos[1] < 0:
            bullets.remove(bullet)


    player_show()
    pygame.display.update()
    clock.tick(150)

    #print(clock.get_fps())
        