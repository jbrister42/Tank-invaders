# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 18:59:54 2020

@author: jbris
"""
import pygame
import random
pygame.init()
clock = pygame.time.Clock()
screen_wid, screen_h = 800,600
screen = pygame.display.set_mode((screen_wid,screen_h))
#screen.fill((255,255,255))
pygame.display.update()

background = pygame.image.load('background.jpg')
repair_img = pygame.image.load('repair.png')
icon = pygame.image.load("tank.png")
pygame.display.set_icon(icon)
font = pygame.font.SysFont(None, 72)
buildimg = pygame.image.load("build.png")

playerimg = pygame.image.load('tank.png')
playerx = 370
playery = 400
vel = 5
upper_lim = 400
full = 800 # Health when full

enemyimg = pygame.image.load('tankbd.png')
en_bullet_img = pygame.image.load('bullet2.png')
explosion = pygame.image.load('explosion.png')
enem_bullets = []
ebull_vel = 10
vel_en2 = 4
vel_en = 2.5
# Boss 
boss_img = pygame.image.load('boss.png')

bullet = pygame.image.load('bullet.png')
bullets = []
bulletx = 0
bullety = 480
bull_vely = 10
bullshot = False

class enemi:
    def __init__(self,x,y,vel,cooldown=0):
        self.x=x
        self.y=y
        self.vel=vel
        self.cooldown=cooldown
    def draw(self):
        blit(enemyimg,self.x,self.y)

class bull:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class explod:
    def __init__(self,x,y,linger=30):
        self.x = x
        self.y = y
        self.linger = linger
        
class powerup:
    def __init__(self,x,y,power):
        self.x = x
        self.y = y 
        self.power = power
    def draw(self):
        blit(repair_img, self.x, self.y)

def boundaries(x,y,width,height):
    if x >= (screen_wid-width):
        x = screen_wid-width
    if x <= (0-10):
        x = -10
    if y <= (upper_lim):
        y = upper_lim
    if y >= (screen_h-height):
        y = screen_h - height
    return x,y

def bounce(x,y,vel,width,height):
    if x >= (800-width):
        x = 800-width
        vel = -vel
        y += 30
    if x <= (0-10):
        x = -10
        vel = -vel
        y += 30
    if y <= (-10):
        y = -10
    if y >= (600-height):
        y = 600 - height
    return vel, y

def bullfire():
    bullets.append(bull(playerx+16,playery-24))

def blit(image,x,y):
    screen.blit(image,(x,y))

# timekeeping
counter = 0
cooldown = 0
load = 0
score = 0

# main loop
enemies = []
explosions = []
is_running = True
Health = full
boss_fight = False
powered = False
while is_running:
    clock.tick(60)
    if not boss_fight: 
        counter += 1
    #timer_img = font.render(str(counter), True, (255,0,0))
    score_img = font.render(str(score),True,(255,255,255))
    if cooldown>0:
        cooldown -= 1
    if load>0:
        load-=1
    if load <= 0:
        size = len(enemies)
        while len(enemies) == size:
            if boss_fight:
                break # if boss fight, end while loop immediately (not spawn enemy tanks)
            collide = False
            new_enemi = enemi(random.randint(80,520),-50,vel_en)
            for enem in enemies:
                if abs(enem.x - new_enemi.x)<64:
                    collide = True
            if not collide:
                enemies.append(new_enemi)
        load = 200 - counter/25
        if load < 50:
            load = 50
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        playerx += vel
    if keys[pygame.K_LEFT]:
        playerx -= vel
    #if keys[pygame.K_DOWN]:
      #  playery += vel
    #if keys[pygame.K_UP]:
     #   playery -= vel
    if keys[pygame.K_SPACE]:
        if cooldown == 0:
            bullfire()
            cooldown = 30
    
    # enemy movement
    for enem in enemies:
        if enem.y<200:
            enem.y+= enem.vel
        #enem.vel,enem.y = bounce(enem.x,enem.y,enem.vel,54,54)
    
    # enemy firing
    for enem in enemies:
        if enem.y >= 200:
            if enem.cooldown == 0:
                enem_bullets.append(bull(enem.x+16,enem.y+64))
                enem.cooldown = 30
            else:
                enem.cooldown -= 1
    
    # Boundaries
    playerx,playery = boundaries(playerx, playery, 54,54)
    
    screen.fill((255,255,255))
    blit(background,0,0)
    
    # player bullets blitting
    for shell in bullets:
        blit(bullet,shell.x,shell.y)
        shell.y -= bull_vely
        if shell.y < 0:
            bullets.remove(shell)
    shellwid=bullet.get_width()
    
    # check if enemies are hit
    enemwid = enemyimg.get_width()
    for shell in bullets:
        for enem in enemies:
            if (abs(shell.x + shellwid/2-(enem.x+enemwid/2)) < shellwid/2+enemwid/2 and (abs(shell.y-enem.y-16)<20)):
                enemies.remove(enem)
                bullets.remove(shell)
                explosions.append(explod(enem.x,enem.y))
                score += 1
        if boss_fight:
            if (abs(shell.x-boss_ob.x-128)<256) and (abs(shell.y-boss_ob.y+128)<256):
                bullets.remove(shell)
                boss_health -= 20
    
    # enemy bullets blitting
    for shell in enem_bullets:
        blit(en_bullet_img, shell.x,shell.y)
        shell.y += ebull_vel
        if shell.y > screen_h:
            enem_bullets.remove(shell)
            Health -= 25
    
    # explosions blitting
    for explo in explosions:
        blit(explosion,explo.x,explo.y)
        explo.linger-=1
        if explo.linger == 0:
            explosions.remove(explo)

    # blit player, enemy tanks and score
    blit(playerimg,playerx,playery)
    blit(score_img, 100,484)
    
    for i in range(12):
        blit(buildimg,16+64*i,600-64)
    
    for enem in enemies:
        blit(enemyimg,enem.x,enem.y)
    
    if (counter>0) and (counter % 500==0):
        power_up = powerup(random.randint(0,540),-40,"health")
        powered = True
    
    if powered:
        power_up.draw()
        power_up.y += 2
        if (abs(playerx+32-power_up.x-16)<48) and (abs(playery+32-power_up.y-16)<48):
            powered = False
            Health = full
        if power_up.y >= 600:
            powered = False
        
    # check if boss round
    if not boss_fight:
        if (score > 0) and (score % 15) == 0:
            boss_fight = True
            boss_health = 200
            boss_ob = enemi(400-128, -256, 1) #***
    # boss blitting
    if boss_fight:
        if boss_ob.cooldown > 0:
            boss_ob.cooldown -= 1
        if boss_ob.y < 50:
            boss_ob.y += 1
        if boss_ob.y >= 50:
            if boss_ob.cooldown == 0:
                enem_bullets.append(bull(boss_ob.x+32,enem.y+64))
                boss_ob.cooldown = 30
            if boss_ob.cooldown == 15:
                enem_bullets.append(bull(boss_ob.x+192,enem.y+64))
                    #boss_ob.cooldown -= 1
                #else:
                 #   boss_ob.cooldown -= 1
    # health check
    pygame.draw.rect(screen,(0,255,0),(0,0,Health,20))
    if Health <= 0:
        is_running = False
    
    # check boss health
    if boss_fight:
        if boss_health <= 0:
            boss_fight = False
            score += 1
            Health = full
    
    # blit boss
    bosstxt = font.render('BOSS',True,(0,0,0))
    if boss_fight:
        blit(bosstxt, 600, 50)
        blit(boss_img, boss_ob.x,boss_ob.y)
        pygame.draw.rect(screen,(255,0,0),(boss_ob.x+32, boss_ob.y - 24,boss_health,20))
    #if not enemies:
     #   is_running= False
    #player-enemy collision detection
    #for enem in enemies:
     #   if (abs(playerx-enem.x-16)<32) and (abs(playery-enem.y-16)<32):
      #      is_running=False
            
    pygame.display.update()

pygame.quit()
