import pygame
from pygame.locals import *

# podstawowe ustawienia
szerokośćOkna = 1024
wysokośćOkna = 896
zegar = None
okno = None
fps = 30

PX = 4 # szerokość piksela
PY = 4 # wysokość piksela
X = 32 # szerokość sprite
Y = 32 # wysokość sprite
klatka = 16.66 # czas trwania klatki w milisekundach

# kontroler NES
# gracz 1
A1 = K_k
B1 = K_l
UP1 = K_UP
DOWN1 = K_DOWN
LEFT1 = K_LEFT
RIGHT1 = K_RIGHT
START1 = K_RETURN
SELECT1 = K_RSHIFT

# gracz 2
A2 = K_k
B2 = K_l
UP2 = K_UP
DOWN2 = K_DOWN
LEFT2 = K_LEFT
RIGHT2 = K_RIGHT
START2 = K_RETURN
SELECT2 = K_RSHIFT

pygame.init()
zegar = pygame.time.Clock ()
okno = pygame.display.set_mode ((szerokośćOkna, wysokośćOkna))
pygame.display.set_caption ("Temtris.py")

# zmienne gry
stan = "gra"

def Intro () :
	pygame.mixer.init()
	
	pygame.time.wait(533)
	
	introSprite = pygame.image.load ("Assets/Grafika/intro sprite.png")
	
	pygame.mixer.music.load ("Assets/Dźwięk/intro.ogg")
	pygame.mixer.music.play ()
	
	for i in range (0, 4) :
		
		# TODO możliwość naciśnięcia START żeby pominąć asynchronicznie kiedy program czeka
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				# START
				if event.key == (START1 or START2) :
					print ("START")
					return
					
		okno.blit(introSprite, Rect (6 * X, 11 * Y, 608, 320), Rect (0, i * 320, 608, 320))
		pygame.display.update ()
		zegar.tick (fps)
		pygame.time.wait(int (32 * klatka))
	
	pygame.time.wait(int (180 * klatka))
	pygame.mixer.music.stop ()

def Menu () :
	
	dwóchGraczy = False
	
	tłoMenu = pygame.image.load ("Assets/Grafika/menu.png")
	okno.blit (tłoMenu, tłoMenu.get_rect())
	
	strzałkaSprite = pygame.image.load ("Assets/Grafika/strzałka.png")
	okno.blit(strzałkaSprite, Rect (5 * X - 2 * PX, 20 * Y, 32, 32))
	
	pygame.mixer.music.load ("Assets/Dźwięk/temtris theme.ogg")
	pygame.mixer.music.play (-1)
	
	while True :
		
		for event in pygame.event.get() :
			
			# naciśnięcie X na oknie
			if event.type == QUIT :
				pygame.quit ()
				exit ()
			
			# naciśnięcie klawisza
			if event.type == KEYDOWN :
				# START
				if event.key == (START1 or START2) :
					print ("START")
					return dwóchGraczy
				elif event.key == (SELECT1 or SELECT2) :
					print ("SELECT")
					dwóchGraczy = not dwóchGraczy
					okno.blit(strzałkaSprite, Rect (5 * X - 2 * PX, 21 * Y, 32, 32))
		
		pygame.display.update ()
		zegar.tick (fps)
	
while True :
	
	Intro ()
	dwóchGraczy = Menu ()
	
	pygame.mixer.music.stop ()
	
	tłoGra = pygame.image.load ("Assets/Grafika/gra.png")
	okno.blit (tłoGra, tłoGra.get_rect())
	
	while stan == "gra" :
		
		for event in pygame.event.get() :
			
			# naciśnięcie X na oknie
			if event.type == QUIT:
				pygame.quit ()
				exit ()
		
		pygame.display.update ()
		zegar.tick (fps)
		
				
	while stan == "koniec gry" :
		
		for event in pygame.event.get() :
			# naciśnięcie X na oknie
			if event.type == QUIT:
				pygame.quit ()
				exit ()
		