import pygame
from pygame.locals import *
from random import randrange

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
A1 = K_l
B1 = K_k
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

# INTRO

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

# MENU

class Strzałka (pygame.sprite.Sprite) :
	
	def __init__(self) :
		super().__init__()
		
		print ("strzałka init")
		self.image = pygame.image.load ("Assets/Grafika/strzałka.png")
		self.rect = self.image.get_rect()
		
def Menu () :
	
	dwóchGraczy = False
	
	# załaduj tło menu
	tłoMenu = pygame.image.load ("Assets/Grafika/menu.png")
	okno.blit (tłoMenu, tłoMenu.get_rect())
	
	# utwórz strzałkę wskazującą na gre dla 1 lub 2 graczy
	strzałka = Strzałka ()
	strzałka.rect.x = 5 * X - 2 * PX
	strzałka.rect.y = 20 * Y
	
	# TODO skoro jest jeden sprite to czy da się to nie robić grupą?
	all_sprites = pygame.sprite.Group()
	all_sprites.add (strzałka)
	all_sprites.draw (okno)
	
	# odtwarzaj muzykę w menu
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
					
					# narysuj tło
					okno.blit (tłoMenu, tłoMenu.get_rect())
					
					if dwóchGraczy :
						strzałka.rect.y += Y
					else :
						strzałka.rect.y -= Y
					
					all_sprites.draw (okno)
		
		pygame.display.update ()
		zegar.tick (fps)

class Klocek (pygame.sprite.Sprite) :
	
	klockiSprite = pygame.image.load ("Assets/Grafika/klocki sprite.png").convert_alpha ()
	
	def __init__ (self, plansza):
		super().__init__()
		
		Klocek.plansza = plansza
		
		# self.numerKlocka = randrange(7)
		self.numerKlocka = 1
		self.obrót = 0
		self.x = 4
		self.y = 0
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (0, self.numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		self.image = grafika
		self.rect = grafika.get_rect ()
		self.rect.x += 13 * X
		self.rect.y += 5 * Y
		
		# TODO jeśli w trakcie tworzenia klocka nastąpiła kolizja to koniec gry
	
	def Opadaj (self) :
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (self.obrót * 128, self.numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		macierzKolizji = []
		
		for y in range (0, 4) :
			macierzKolizji.append ([])
			for x in range (0, 4) :
				if grafika.get_at ((x * 32, y * 32)) == (0, 0, 0, 255) :
					macierzKolizji[y].append (0)
				else :
					macierzKolizji[y].append (1)
		
		if Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y + 1) :
			
			print ("kolizja, umieść klocek")
			
		else :
			self.rect.y += Y
			self.y += 1
	
	def PrzesuńWPrawo (self) :
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (self.obrót * 128, self.numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		macierzKolizji = []
		
		for y in range (0, 4) :
			macierzKolizji.append ([])
			for x in range (0, 4) :
				if grafika.get_at ((x * 32, y * 32)) == (0, 0, 0, 255) :
					macierzKolizji[y].append (0)
				else :
					macierzKolizji[y].append (1)
		
		if Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x + 1, self.y) :
			
			print ("kolizja, nie można przesunąć")
			
		else :
			self.rect.x += X
			self.x += 1
		
	def PrzesuńWLewo (self) :
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (self.obrót * 128, self.numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		macierzKolizji = []
		
		for y in range (0, 4) :
			macierzKolizji.append ([])
			for x in range (0, 4) :
				if grafika.get_at ((x * 32, y * 32)) == (0, 0, 0, 255) :
					macierzKolizji[y].append (0)
				else :
					macierzKolizji[y].append (1)
		
		if Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x - 1, self.y) :
			
			print ("kolizja, nie można przesunąć")
			
		else :
			self.rect.x -= X
			self.x -= 1
	
	def ObróćWPrawo (self) :
		
		self.obrót = (self.obrót + 1) % 4
		print ("obrót: " + str (self.obrót))
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (self.obrót * 128, self.numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		self.image = grafika
		
	def ObróćWLewo (self) :
		self.obrót = (self.obrót - 1) % 4
		print ("obrót: " + str (self.obrót))
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (self.obrót * 128, self.numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		self.image = grafika
		

class Plansza () :
	
	def __init__ (self) :
		
		self.macierzSpriteów = [[0 for x in range(10)] for y in range(20)]
		print (self.macierzSpriteów)
		
	def Wyświetl (self) :
		print ("placeholder")
		# przejdź przez wszystkie sprite na planszy i narysuj
	
	def SprawdźRozbicieLinii (self) :
		print ("placeholder")
		
	def SprawdźKolizję (self, macierzKolizji, x, y) :
		
		print ("sprawdzanie kolizji w punkcie (" + str (x) + ", " + str (y) + ")")
		
		self.DebugPokażMapeKolizji (macierzKolizji, x, y)
		
		for sx in range (0, 4) :
			for sy in range (0, 4) :
				
				# fragment klocka wyszedł za plansze, czyli mamy kolizję ze ścianą
				if macierzKolizji[sx][sy] == 1 and (sx > 19 or sx < 0 or sy > 19) :
					return True
				
				if sx < 0 or sx > 9 or sy > 19 :
					continue
				
				if self.macierzSpriteów[sx + x][sy + y] > 0 and macierzKolizji[sx, sy] == 1 :
					print ("macierz spriteów = " + str (self.macierzSpriteów[sx + x][sy + y]))
					print ("macierz kolizji = " + str (self.macierzSpriteów[sx][sy]))
					return True
		
		return False

	def DebugPokażMapeKolizji (self, macierzKolizji, x, y) :
		
		kx = x - 9
		ky = -1 - y
		
		for sy in range (0, 20) :
			print ()
			kx = x - 9
			for sx in range (0, 10) :
				if sy > y and sy <= y + 4 :
					if sx > x and sx <= x + 4 :
						print ("(" + str(kx) + ", " + str(ky) + ")")
						print ('\033[93m' + str (self.macierzSpriteów[sy][sx] + macierzKolizji[ky][kx]) + '\033[0m', end=", ")
					else :
						print (self.macierzSpriteów[sy][sx], end=", ")
				else :
					print (self.macierzSpriteów[sy][sx], end=", ")
				
				kx += 1
			ky += 1
		
		print ()

def Gra (dwóchGraczy) :
	
	pygame.mixer.music.stop ()
	
	tłoGra = pygame.image.load ("Assets/Grafika/gra.png")
	okno.blit (tłoGra, tłoGra.get_rect())
	
	plansza = Plansza ()
	
	while True :
		
		# stwórz klocek i stwórz następny klocek
		
		obecnyKolcek = Klocek (plansza)
		
		all_sprites = pygame.sprite.Group ()
		all_sprites.add (obecnyKolcek)
		all_sprites.draw (okno)
		
		# opadanie klocka
		
		while True :
			
			for event in pygame.event.get() :
				
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
				
				if event.type == KEYDOWN :
					if event.key == A1 :
						print ("A")
						obecnyKolcek.ObróćWPrawo ()
						
					elif event.key == B1 :
						print ("B")
						obecnyKolcek.ObróćWLewo ()
						
					elif event.key == RIGHT1 :
						print ("RIGHT")
						obecnyKolcek.PrzesuńWPrawo ()
						
					elif event.key == DOWN1 :
						print ("DOWN")
						obecnyKolcek.Opadaj ()
						
					elif event.key == LEFT1 :
						print ("LEFT")
						obecnyKolcek.PrzesuńWLewo ()
			
			okno.blit (tłoGra, tłoGra.get_rect())
			all_sprites.draw (okno)
			pygame.display.update ()
			zegar.tick (fps)
		
		# umieszczanie klocka
		
		# sprawdzanie linii
		
		okno.blit (tłoGra, tłoGra.get_rect())
		all_sprites.draw (okno)
		pygame.display.update ()
		zegar.tick (fps)

def KoniecGry () :
	
	while True :
		
		for event in pygame.event.get() :
			# naciśnięcie X na oknie
			if event.type == QUIT:
				pygame.quit ()
				exit ()

# główna pętla
while True :
	
	Intro ()
	dwóchGraczy = Menu ()
	Gra (dwóchGraczy)
	KoniecGry ()
