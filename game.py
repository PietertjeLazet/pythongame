import pygame
from sys import exit
from pygame.locals import *
from pygame import mixer
import random

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

biem_sound = pygame.mixer.Sound("biem.mp3")

def player_setup():
    global player_pos
    player.append(int(800))
    player.append(int(700))
    player_pos = pygame.Vector2(player[0], player[1])
    
player_setup() 

game_over_font = pygame.font.Font(None, 100)
game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(800, 400))

you_won_font = pygame.font.Font(None, 100)
you_won_text = you_won_font.render("You Won", True, (0, 255, 0))
you_won_rect = you_won_text.get_rect(center=(800, 400))


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
        self.radius = 5  

    def draw(self, window):
        window.blit(self.img, (int(self.pos[0]), int(self.pos[1])))

    def update(self):
        self.pos = (self.pos[0], self.pos[1] - self.vel)
        
class Enemy:
    def __init__(self, pos):
        self.pos = pos
        self.vel = 0.05
        self.Hvel = 10
        self.width = 10
        self.height = 30
        self.radius = 20
        self.img = pygame.image.load("kaag.jpg")
        self.img = pygame.transform.scale(self.img, (40, 40))

    def draw(self, window):
        window.blit(self.img, (int(self.pos[0] - self.img.get_width() / 2), int(self.pos[1] - self.img.get_height() / 2)))

    def update(self):
        self.pos = (self.pos[0], self.pos[1] + self.vel)

    def move_horizontally(self):
        self.pos = (self.pos[0] + self.Hvel, self.pos[1])
        self.Hvel = self.Hvel * -1

class EnemyBullet:
    def __init__(self, pos, vel, img):
        self.pos = pos
        self.vel = 2 
        self.img = img
        self.radius = 5

    def draw(self, window):
        window.blit(self.img, (int(self.pos[0]), int(self.pos[1])))

    def update(self):
        self.pos = (self.pos[0], self.pos[1] + self.vel)
        
enemy_bullets = []
enemy_shoot_timer = 0
        
for j in range(4):
    for i in range(10):
        enemies.append(Enemy([40 + i*160, 30 + j*60]))

game_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            game_started = True
            
    if not game_started:
        start_font = pygame.font.Font(None, 80)
        start_text = start_font.render("Click 'Start' to play", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(800, 400))
        screen.blit(start_text, start_rect)
        
    else:
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
                biem_sound.play()
        if keys[pygame.K_u]:
            enemy.play()
        if keys[pygame.K_r]:
            shot.play()
            pygame.time.delay(2000)
            

        
        for bullet in bullets:
            bullet.update()
            bullet.draw(screen)
        for enemy in enemies:
            enemy.move_horizontally()
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


        if pygame.time.get_ticks() - enemy_shoot_timer >= 1000:
            random_enemy = random.choice(enemies)
            enemy_bullets.append(EnemyBullet(random_enemy.pos, 1, bullet_img))
            enemy_shoot_timer = pygame.time.get_ticks()

        for enemy_bullet in enemy_bullets:
            enemy_bullet.update()
            enemy_bullet.draw(screen)

        for enemy_bullet in enemy_bullets[:]:
            dist = ((enemy_bullet.pos[0] - player_pos.x)**2 + (enemy_bullet.pos[1] - player_pos.y)**2)**0.5
            if dist < enemy_bullet.radius + rect.width / 2:
                enemy_bullets.remove(enemy_bullet)
                screen.blit(game_over_text, game_over_rect)
                pygame.display.update()
                pygame.time.delay(5000)
                pygame.quit()
                exit()
            if enemy_bullet.pos[1] > 800:
                enemy_bullets.remove(enemy_bullet)
        
        for enemy in enemies:
            if enemy.pos[1] > 550:
                screen.blit(game_over_text, game_over_rect)
                pygame.display.update()
                pygame.time.delay(5000)
                pygame.quit()
                exit()
        
        if not enemies:
            mixer.music.stop()
            screen.blit(you_won_text, you_won_rect)
            pygame.display.update()
            mixer.music.load('wildersminderkaag.mp3')
            mixer.music.play()
            pygame.time.delay(5000)
            pygame.quit()
            exit()
        
        
        player_show()
    pygame.display.update()    
    clock.tick(150)
        
