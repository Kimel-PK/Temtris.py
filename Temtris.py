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
	
	# TODO czy da się to uprościć?
	# czekaj 32 klatki
	for _ in range (0, 16) :
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				# START
				if event.key == (START1 or START2) :
					print ("START")
					return
		
		pygame.display.update ()
		zegar.tick (fps)
	
	introSprite = pygame.image.load ("Assets/Grafika/intro sprite.png")
	
	pygame.mixer.music.load ("Assets/Dźwięk/intro.ogg")
	pygame.mixer.music.play ()
	
	for i in range (0, 4) :
		
		okno.blit(introSprite, Rect (6 * X, 11 * Y, 608, 320), Rect (0, i * 320, 608, 320))
		
		# czekaj 32 klatki
		for _ in range (0, 16) :
			# TODO czy da się to uprościć?
			for event in pygame.event.get() :
				if event.type == KEYDOWN :
					# START
					if event.key == (START1 or START2) :
						print ("START")
						return
			
			pygame.display.update ()
			zegar.tick (fps)
	
	# czekaj 180 klatek
	for _ in range (0, 90) :
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				# START
				if event.key == (START1 or START2) :
					print ("START")
					return
		
		pygame.display.update ()
		zegar.tick (fps)
		
	pygame.mixer.music.stop ()

# MENU

class Strzałka (pygame.sprite.Sprite) :
	
	def __init__(self) :
		super().__init__()
		
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
	wszystkieSprite = pygame.sprite.Group()
	wszystkieSprite.add (strzałka)
	wszystkieSprite.draw (okno)
	
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
					
					wszystkieSprite.draw (okno)
		
		pygame.display.update ()
		zegar.tick (fps)

class Klocek (pygame.sprite.Sprite) :
	
	klockiSprite = pygame.image.load ("Assets/Grafika/klocki sprite.png").convert_alpha ()
	
	def __init__ (self, plansza) :
		super().__init__()
		
		Klocek.plansza = plansza
		
		self.numerKlocka = randrange(7)
		self.obrót = 0
		
		self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		self.rect = self.image.get_rect ()
	
	def UstawPozycję (self, x, y) :
		
		self.x = x - 10
		self.y = y - 5
		
		print ("ustawianie pozycji na: (" + str (self.x) + ", " + str (self.y) + ")")
		
		self.rect.x = x * X
		self.rect.y = y * Y
		
		if Klocek.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x, self.y) :
			return False
		else :
			return True
	
	def UtwórzGrafike (self, obrót, numerKlocka) -> pygame.Surface :
		
		grafika = pygame.Surface((128, 128)).convert_alpha ()
		grafika.blit (Klocek.klockiSprite, Rect (0, 0, 128, 128), Rect (obrót * 128, numerKlocka * 128, 128, 128))
		grafika.set_colorkey ((0, 0, 0))
		
		return grafika
	
	def UtwórzMacierzKolizji (self, grafika) :
		
		macierzKolizji = []
		
		for y in range (0, 4) :
			macierzKolizji.append ([])
			for x in range (0, 4) :
				if grafika.get_at ((x * 32 + 16, y * 32 + 16)) == (0, 0, 0, 255) :
					macierzKolizji[y].append (0)
				else :
					macierzKolizji[y].append (1)
		
		return macierzKolizji
	
	def Opadaj (self) :
		
		if Klocek.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x, self.y + 1) :
			
			print ("kolizja, umieść klocek")
			return False
		else :
			self.rect.y += Y
			self.y += 1
			
			return True
	
	def PrzesuńWPrawo (self) :
		
		if Klocek.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x + 1, self.y) :
			
			print ("kolizja, nie można przesunąć")
			
		else :
			self.rect.x += X
			self.x += 1
		
	def PrzesuńWLewo (self) :
		
		if Klocek.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x - 1, self.y) :
			print ("kolizja, nie można przesunąć")
		else :
			self.rect.x -= X
			self.x -= 1
	
	def ObróćWPrawo (self) :
		
		obrót = (self.obrót + 1) % 4
		print ("obrót: " + str (self.obrót))
		
		macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
		
		self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		
		if Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
			print ("kolizja, nie można przesunąć")
		else :
			self.obrót = (self.obrót + 1) % 4
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		
	def ObróćWLewo (self) :
		
		obrót = (self.obrót - 1) % 4
		print ("obrót: " + str (self.obrót))
		
		macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
		
		self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		
		if Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
			print ("kolizja, nie można przesunąć")
		else :
			self.obrót = (self.obrót - 1) % 4
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)

class Fragment (pygame.sprite.Sprite) :
	
	fragmentySprite = pygame.image.load ("Assets/Grafika/fragmenty sprite.png").convert_alpha ()
	
	def __init__ (self, numerFragmentu, x, y) :
		super().__init__()
		
		self.numerFragmentu = numerFragmentu
		
		self.UstawGrafikę (0, self.numerFragmentu)
		self.rect = self.image.get_rect ()
		self.rect.x = x * X + 10 * X
		self.rect.y = y * Y + 5 * Y
		
	def UstawGrafikę (self, numerGracza, numerFragmentu) -> pygame.Surface :
		
		# numer gracza nakłada na fragment specyficzny kolor
		# jeśli numer gracza == 0 to nakłada kolor poziomu
		# jeśli nie da się osiągnąc przez nakładanie takich kolorów to zrobię spritesheeta z wszystkimi kolorami ręcznie
		
		grafika = pygame.Surface((32, 32)).convert_alpha ()
		grafika.blit (Fragment.fragmentySprite, Rect (0, 0, 32, 32), Rect (numerFragmentu * 32, 0, 32, 32))
		grafika.set_colorkey ((0, 0, 0))
		
		self.image = grafika
	
class Plansza () :
	
	def __init__ (self) :
		
		self.macierzSpriteów = [[None for x in range(10)] for y in range(20)]
		print (self.macierzSpriteów)
		
	def Rysuj (self) :
		
		wszystkieSprite = pygame.sprite.Group ()
		
		for y in range (0, 20) :
			for x in range (0, 10) :
				if self.macierzSpriteów[y][x] != None :
					wszystkieSprite.add (self.macierzSpriteów[y][x])
		
		wszystkieSprite.draw (okno)
	
	def SprawdźRozbicieLinii (self) :
		
		linie = []
		
		for y in range (0, 20) :
			rozbita = True
			for x in range (0, 10) :
				if self.macierzSpriteów[y][x] == None :
					rozbita = False
					break
			if rozbita :
				linie.append (y)
		
		return linie
		
	def SprawdźKolizję (self, macierzKolizji, x, y) :
		
		print ("sprawdzanie kolizji w punkcie (" + str (x) + ", " + str (y) + ")")
		
		for sy in range (0, 4) :
			for sx in range (0, 4) :
				
				# fragment klocka wyszedł za plansze, czyli mamy kolizję ze ścianą
				if macierzKolizji[sy][sx] == 1 and (x + sx < 0 or x + sx > 9 or y + sy > 19) :
					print ("kolizja wyjście klocka za plansze")
					return True
				
				if x + sx < 0 or x + sx > 9 or y + sy > 19 :
					continue
				
				if self.macierzSpriteów[y + sy][x + sx] != None and macierzKolizji[sy][sx] == 1 :
					return True
		
		print ("brak kolizji")
		return False
	
	def UmieśćKlocek (self, macierzKolizji, x, y) :
		
		print ("umieść klocek na (" + str (x) + "," + str (y) + ")")
		
		for sy in range (0, 4) :
			for sx in range (0, 4) :
				
				if macierzKolizji[sy][sx] == 1 :
					# tworzymy nowy Fragment
					
					numerFragmentu = 0
					
					# ustalamy grafikę fragmentu
					
					# inny fragment z góry
					if sy - 1 >= 0 and macierzKolizji[sy - 1][sx] == 1 :
						numerFragmentu += 8
					# inny fragment z prawej
					if sx + 1 < 4 and macierzKolizji[sy][sx + 1] == 1 :
						numerFragmentu += 4
					# inny fragment z dołu
					if sy + 1 < 4 and macierzKolizji[sy + 1][sx] == 1 :
						numerFragmentu += 2
					# inny fragment z prawej
					if sx - 1 >= 0 and macierzKolizji[sy][sx - 1] == 1 :
						numerFragmentu += 1
					
					self.macierzSpriteów[y + sy][x + sx] = Fragment (numerFragmentu, x + sx, y + sy)
	
	def RozbijLinie (self, linieDoRozbicia) :
		
		print ("rozbijanie linii")
		
		# odtwórz animację
		
		for _ in range (0, 60) :
			
			pygame.display.update ()
			zegar.tick (fps)
		
		# zmień grafiki
		
		for numerLinii in linieDoRozbicia :
			if numerLinii - 1 >= 0 :
				for x in range (0, 10) :
					if self.macierzSpriteów [numerLinii][x] != None :
						self.macierzSpriteów[numerLinii][x].UstawGrafikę (0, self.macierzSpriteów[numerLinii][x].numerFragmentu & 13)
			
			if numerLinii + 1 < 20 :
				for x in range (0, 10) :
					if self.macierzSpriteów [numerLinii][x] != None :
						self.macierzSpriteów[numerLinii][x].UstawGrafikę (0, self.macierzSpriteów[numerLinii][x].numerFragmentu & 7)
		
		# usuń linie i utwórz nowe na górze
		for numerLinii in linieDoRozbicia :
			print ("usuń linię " + str (numerLinii))
			del self.macierzSpriteów [numerLinii]
			self.macierzSpriteów.insert (0, [])
			for _ in range (0, 10) :
				self.macierzSpriteów[0].append (None)
		
		for y in range (0, 20) :
			for x in range (0, 10) :
				if self.macierzSpriteów [y][x] != None :
					self.macierzSpriteów [y][x].rect.y = y * Y + 5 * Y
	
	def DebugPokażMapeKolizji (self, macierzKolizji, x, y) :
		
		ky = -y
		
		for sy in range (0, 20) :
			kx = -x
			print ()
			for sx in range (0, 10) :
				if ky >= 0 and ky < 4 :
					if kx >= 0 and kx < 4 :
						if self.macierzSpriteów[sy][sx] != None :
							if self.macierzSpriteów[sy][sx].numerFragmentu < 10 :
								print ('\033[93m' + "0" + str (self.macierzSpriteów[sy][sx].numerFragmentu + macierzKolizji[ky][kx]) + '\033[0m', end=", ")
							else :
								print ('\033[93m' + str (self.macierzSpriteów[sy][sx].numerFragmentu + macierzKolizji[ky][kx]) + '\033[0m', end=", ")
						else :
							print ('\033[93m' + "0" + str (macierzKolizji[ky][kx]) + '\033[0m', end=", ")
					else :
						if self.macierzSpriteów[sy][sx] != None :
							if self.macierzSpriteów[sy][sx].numerFragmentu < 10 :
								print ("0" + str (self.macierzSpriteów[sy][sx].numerFragmentu), end=", ")
							else :
								print (self.macierzSpriteów[sy][sx].numerFragmentu, end=", ")
						else :
							print ("--", end=", ")
				else :
					if self.macierzSpriteów[sy][sx] != None :
						if self.macierzSpriteów[sy][sx].numerFragmentu < 10 :
								print ("0" + str (self.macierzSpriteów[sy][sx].numerFragmentu), end=", ")
						else :
							print (self.macierzSpriteów[sy][sx].numerFragmentu, end=", ")
					else :
						print ("--", end=", ")
				
				kx += 1
			ky += 1
		
		print ()

def Gra (dwóchGraczy) :
	
	pygame.mixer.music.stop ()
	
	tłoGra = pygame.image.load ("Assets/Grafika/gra.png")
	okno.blit (tłoGra, tłoGra.get_rect())
	
	plansza = Plansza ()
	następnyKolcek = Klocek (plansza)
	następnyKolcek.UstawPozycję (4, 4)
	
	while True :
		
		# stwórz obecny i następny klocek
		
		obecnyKlocek = następnyKolcek
		if not obecnyKlocek.UstawPozycję (13, 5) :
			break
		następnyKolcek = Klocek (plansza)
		następnyKolcek.UstawPozycję (4, 4)
		
		wszystkieSprite = pygame.sprite.Group()
		wszystkieSprite.add (obecnyKlocek)
		wszystkieSprite.add (następnyKolcek)
		wszystkieSprite.draw (okno)
		
		# opadanie klocka
		
		opadanie = True
		
		while opadanie :
			
			for event in pygame.event.get() :
				
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
				
				if event.type == KEYDOWN :
					if event.key == A1 :
						print ("A")
						obecnyKlocek.ObróćWPrawo ()
						
					elif event.key == B1 :
						print ("B")
						obecnyKlocek.ObróćWLewo ()
						
					elif event.key == RIGHT1 :
						print ("RIGHT")
						obecnyKlocek.PrzesuńWPrawo ()
						
					elif event.key == DOWN1 :
						print ("DOWN")
						if not obecnyKlocek.Opadaj () :
							opadanie = False
						
					elif event.key == LEFT1 :
						print ("LEFT")
						obecnyKlocek.PrzesuńWLewo ()
						
					print ("pozycja klocka (" + str (obecnyKlocek.x) + ", " + str (obecnyKlocek.y) + ")")
					Klocek.plansza.DebugPokażMapeKolizji (obecnyKlocek.UtwórzMacierzKolizji(obecnyKlocek.image), obecnyKlocek.x, obecnyKlocek.y)
			
			# klawisze = pygame.key.get_pressed()  #checking pressed keys
			# if keys[pygame.K_UP]:
			# 	y1 -= 1
			# if keys[pygame.K_DOWN]:
			# 	y1 += 1
			
			okno.blit (tłoGra, tłoGra.get_rect())
			wszystkieSprite.draw (okno)
			plansza.Rysuj ()
			pygame.display.update ()
			zegar.tick (fps)
		
		# umieszczanie klocka
		plansza.UmieśćKlocek (obecnyKlocek.UtwórzMacierzKolizji (obecnyKlocek.image), obecnyKlocek.x, obecnyKlocek.y)
		
		# sprawdzanie linii
		linieDoRozbicia = plansza.SprawdźRozbicieLinii ()
		
		if len (linieDoRozbicia) > 0 :
			plansza.RozbijLinie (linieDoRozbicia)
			
		# odśwież ekran
		okno.blit (tłoGra, tłoGra.get_rect())
		wszystkieSprite.draw (okno)
		plansza.Rysuj ()
		pygame.display.update ()
		zegar.tick (fps)

def KoniecGry () :
	
	while True :
		
		pygame.mixer.music.stop ()
		
		# TODO czy da się to uprościć?
		# czekaj 32 klatki
		for _ in range (0, 16) :
			
			pygame.display.update ()
			zegar.tick (fps)
		
		koniecGryKlatka1 = pygame.image.load ("Assets/Grafika/koniec gry klatka 1.png")
		koniecGryKlatka2 = pygame.image.load ("Assets/Grafika/koniec gry klatka 2.png")
		
		pygame.mixer.music.load ("Assets/Dźwięk/koniec gry.ogg")
		pygame.mixer.music.play ()
		
		okno.blit (koniecGryKlatka1, koniecGryKlatka1.get_rect())
		pygame.display.update ()
		zegar.tick (fps)
		
		for _ in range (0, 42) :
			
			pygame.display.update ()
			zegar.tick (fps)
		
		okno.blit (koniecGryKlatka2, koniecGryKlatka2.get_rect())
		pygame.display.update ()
		zegar.tick (fps)
		
		while True :
		
			for event in pygame.event.get() :
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
					
				if event.type == KEYDOWN :
					if event.key == (START1 or START2) :
						return
			
			pygame.display.update ()
			zegar.tick (fps)

Intro ()

# główna pętla
while True :
	
	dwóchGraczy = Menu ()
	Gra (dwóchGraczy)
	KoniecGry ()
