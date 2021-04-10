import pygame
import random
import math
from pygame import mixer
# Initializing the Pygame
pygame.init()

# Creating te screen
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load('Background.jpg')


#background sound
mixer.music.load('space.mp3')
mixer.music.play(-1)


# titile and Icon
pygame.display.set_caption('Space Invader')
icon=pygame.image.load('rocket.png')
pygame.display.set_icon(icon)



# player
playerimg=pygame.image.load('spaceship.png')

playerx=370
playery=480
playerx_change=0

#enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
no_of_enemies=10

for i in range(no_of_enemies):
	enemyimg.append(pygame.image.load('coronavirus.png'))
	enemyx.append(random.randint(0,735))
	enemyy.append(random.randint(50,150))
	enemyx_change.append(4)
	enemyy_change.append(40)


#Bullet
#ready cant see the bullet
#fire can see the bullet moving

bulletimg=pygame.image.load('bullet.png')
bulletx=0
bullety=480
bulletx_change=0
bullety_change=10
bullet_state='ready'

#score
score_value = 0
font=pygame.font.Font('freesansbold.ttf',32)

textx=10
texty=10


#gameover text

over_font=pygame.font.Font('freesansbold.ttf',64)


def game_over_text():
	over_text=over_font.render('GAME OVER',True,(255,255,255))
	screen.blit(over_text,(200,250))

def show_score(x,y):
	score=font.render('Score :'+str(score_value),True,(255,255,255))
	screen.blit(score,(x,y))

#player img
def player(x,y):
	screen.blit(playerimg,(x,y))
	
#enemy img
def enemy(x,y,i):
	screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state='fire'
	screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyx,enemyy,bulletx,bullety):
	distance=math.sqrt((enemyx-bulletx)**2+(enemyy-bullety)**2)
	if distance < 27 :
		return True
	else :
		return False


# Game Loop
running=True
while running :
	screen.fill((0,0,0))
	#background image
	screen.blit(background,(0,0))
	# print(playerx)
	for event in pygame.event.get():
		if event.type == pygame.QUIT :
			running = False
		if event.type == pygame.KEYDOWN :
			if event.key ==	pygame.K_LEFT :
				playerx_change=-5
				print('Left arrow pressed')
			if event.key ==	pygame.K_RIGHT :
				playerx_change=5
				print('Right arrow pressed')
				
			if event.key ==	pygame.K_SPACE :
				if bullet_state is 'ready' :
					bullet_sound=mixer.Sound('laser.wav')
					bullet_sound.play()
					#get the current x coordinate
					bulletx=playerx
					print('Space Pressed')
					fire_bullet(bulletx,bullety)
			
		if event.type == pygame.KEYUP :
			if event.key ==	pygame.K_LEFT or  event.key == pygame.K_RIGHT :
				print('Keystroke released')
				playerx_change=0.0
				
	#Checking player of boundaries			
	playerx+=playerx_change 
	if playerx <= 0 :
		playerx=0
	elif playerx >= 736 :
		playerx=736
	
	#Enemy Movement
	for i in range(no_of_enemies):
		
		#Game over
		if enemyy[i] > 440 :
			for j in range(no_of_enemies) :
				enemyy[j] = 2000
			game_over_text()
			break
		enemyx[i]+=enemyx_change[i]
		if enemyx[i] <= 0 :
			enemyx_change[i]=4
			enemyy[i]+=enemyy_change[i]
		elif enemyx[i] >= 736 :
			enemyx_change[i]=-4
			enemyy[i]+=enemyy_change[i]	
		
		collision=iscollision(enemyx[i],enemyy[i],bulletx,bullety)
		#collision
		if collision :
			collision_sound=mixer.Sound('explosion.wav')
			collision_sound.play()
			bullety=480
			bullet_state='ready'
			score_value+=1
			enemyx[i]=random.randint(0,735)
			enemyy[i]=random.randint(50,150)
		
		enemy(enemyx[i],enemyy[i],i)
		
		
	
	#bullet movement
	if bullety <= 0:
		bullety=480
		bullet_state='ready'
	if bullet_state is 'fire' :
		fire_bullet(bulletx,bullety)
		bullety-=bullety_change
		
	player(playerx,playery)
	
	show_score(textx,texty)
	
	pygame.display.update()

