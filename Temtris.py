# #####################################################################################################
# 
# ┌──────────────────┐                                    ┌──┐
# └───────┐  ┌───────┘                                    │  │
#         │  │                                       ─────┘  └──┐                 ┌──┐
#         │  │                                     /──────┐  ┌──┘                 └──┘
#         │  │    ┌──────────┐                            │  │
#         │  │    │  ┌───────┘    ┌────────────────       │  │    |\    ─────┐    ┌──┐      ────────
#         │  │    │  │            │  ┌────┐  ┌────┐ \     │  │    │ \ /   ───┘    │  │    /   ───────\
#         │  │    │  └───┐        │  │    │  │    │  │    │  │    │     /         │  │     \  \
#         │  │    │  ┌───┘        │  │    │  │    │  │    │  │    │   /           │  │        \  \
#         │  │    │  │            │  │    │  │    │  │    │  │    │  │            │  │           \  \
#         │  │    │  └───────┐    │  │    │  │    │  │    │  │    │  │            │  │     ─────     /
#         │  │    └──────────┘    └──┘    └──┘    └──┘    └──┘    └──┘            └──┘     \────────/
#         │ /
#         │/
# 
# #####################################################################################################
#                                                       Port Temtris 1.5.4 (NES) => Temtris.py (Python)
#                                              https://github.com/Kimel-PK/Temtris
#                                                                                              Kimel_PK
# #####################################################################################################

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
# TODO zrobić favicona
pygame.display.set_caption ("Temtris.py")

pauza = False
poziom = 0
liczbaLinii = 0
liczbaLiniiCheems = 0
liczbaLiniiDoge = 0
liczbaLiniiBuffDoge = 0
liczbaLiniiTemtris = 0
czasGry = 0
obecnyGracz = 0
zegarKontrolera = 10
szybkośćOpadaniaKlocka = 60
zegarOpadania = 60

uderzenieSFX = pygame.mixer.Sound("Assets/Dźwięk/uderzenie.ogg")

cheemsSFX = pygame.mixer.Sound("Assets/Dźwięk/cheems.ogg")
dogeSFX = pygame.mixer.Sound("Assets/Dźwięk/doge.ogg")
buffdogeSFX = pygame.mixer.Sound("Assets/Dźwięk/buffdoge.ogg")
temtrisSFX = pygame.mixer.Sound("Assets/Dźwięk/temtris.ogg")

muzyka = [
	"Assets/Dźwięk/Never Gonna Give You Up NES APU cover.ogg",
	"Assets/Dźwięk/Together Forever NES APU cover.ogg",
	"Assets/Dźwięk/Song For Denise NES APU cover.ogg",
	"Assets/Dźwięk/Szanty Bitwa NES APU cover.ogg"
]

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
						return
			
			pygame.display.update ()
			zegar.tick (fps)
	
	# czekaj 180 klatek
	for _ in range (0, 90) :
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				# START
				if event.key == (START1 or START2) :
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
			return False
		else :
			self.rect.y += Y
			self.y += 1
			
			return True
	
	def PrzesuńWPrawo (self) :
		
		if not Klocek.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x + 1, self.y) :
			self.rect.x += X
			self.x += 1
		
	def PrzesuńWLewo (self) :
		
		if not Klocek.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x - 1, self.y) :
			self.rect.x -= X
			self.x -= 1
	
	def ObróćWPrawo (self) :
		
		# TODO obrót z przesunięciem
		
		obrót = (self.obrót + 1) % 4
		
		macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
		
		self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		
		if not Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
			self.obrót = (self.obrót + 1) % 4
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		
	def ObróćWLewo (self) :
		
		# TODO obrót z przesunięciem
		
		obrót = (self.obrót - 1) % 4
		
		macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
		
		self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
		
		if not Klocek.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
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

class AnimacjaRozbijanejLinii (pygame.sprite.Sprite) :
	
	rozbijanieLiniiSprite = pygame.image.load ("Assets/Grafika/rozbijanie linii sprite.png").convert_alpha ()
	
	def __init__ (self, ilośćLinii, numerLinii) :
		super ().__init__ ()
		
		self.klatka = -1
		self.ilośćLinii = ilośćLinii
		
		self.NastępnaKlatka ()
		self.rect = self.image.get_rect ()
		self.rect.x = 10 * X
		self.rect.y = 5 * Y + numerLinii * Y
	
	def NastępnaKlatka (self) :
		
		self.klatka += 1
		
		grafika = pygame.Surface((320, 32)).convert_alpha ()
		grafika.blit (AnimacjaRozbijanejLinii.rozbijanieLiniiSprite, Rect (0, 0, 320, 32), Rect ((self.ilośćLinii - 1) * 320, self.klatka * 32, 320, 32))
		grafika.set_colorkey ((0, 255, 0))
		
		self.image = grafika
		
class Plansza () :
	
	def __init__ (self) :
		self.macierzSpriteów = [[None for x in range(10)] for y in range(20)]
		
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
		
		for sy in range (0, 4) :
			for sx in range (0, 4) :
				
				# wyszliśmy po za planszę
				if x + sx < 0 or x + sx > 9 or y + sy > 19 :
					# fragment klocka wyszedł za plansze, czyli mamy kolizję ze ścianą
					if macierzKolizji[sy][sx] == 1 :
						return True
					continue
				
				if self.macierzSpriteów[y + sy][x + sx] != None and macierzKolizji[sy][sx] == 1 :
					return True
		
		return False
	
	def UmieśćKlocek (self, macierzKolizji, x, y) :
		
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
					
		pygame.mixer.Sound.play(uderzenieSFX)
	
	def RozbijLinie (self, linieDoRozbicia) :
		
		# odtwórz animację
		
		spriteAnimacji = pygame.sprite.Group ()
		
		for numerLinii in linieDoRozbicia :
			spriteAnimacji.add (AnimacjaRozbijanejLinii (len (linieDoRozbicia), numerLinii))
		
		global liczbaLinii
		liczbaLinii += len (linieDoRozbicia)
		
		if len (linieDoRozbicia) == 1 :
			pygame.mixer.Sound.play(cheemsSFX)
			global liczbaLiniiCheems
			liczbaLiniiCheems += 1
		elif len (linieDoRozbicia) == 2 :
			pygame.mixer.Sound.play(dogeSFX)
			global liczbaLiniiDoge
			liczbaLiniiDoge += 1
		elif len (linieDoRozbicia) == 3 :
			pygame.mixer.Sound.play(buffdogeSFX)
			global liczbaLiniiBuffDoge
			liczbaLiniiBuffDoge += 1
		elif len (linieDoRozbicia) == 4 :
			pygame.mixer.Sound.play(temtrisSFX)
			global liczbaLiniiTemtris
			liczbaLiniiTemtris += 1
		
		for x in range (0, 32) :
			
			# self.Rysuj ()
			spriteAnimacji.draw (okno)
			
			pygame.display.update ()
			zegar.tick (fps * 2)
			
			for sprite in spriteAnimacji :
				sprite.NastępnaKlatka ()
		
		# zmień grafiki
		
		for numerLinii in linieDoRozbicia :
			if numerLinii - 1 >= 0 :
				for x in range (0, 10) :
					if self.macierzSpriteów [numerLinii - 1][x] != None :
						self.macierzSpriteów[numerLinii - 1][x].UstawGrafikę (0, self.macierzSpriteów[numerLinii - 1][x].numerFragmentu & 13)
			
			if numerLinii + 1 < 20 :
				for x in range (0, 10) :
					if self.macierzSpriteów [numerLinii + 1][x] != None :
						self.macierzSpriteów[numerLinii + 1][x].UstawGrafikę (0, self.macierzSpriteów[numerLinii + 1][x].numerFragmentu & 7)
		
		# usuń linie i utwórz nowe na górze
		for numerLinii in linieDoRozbicia :
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

def OdtwarzajMuzykę () :
	
	if not pygame.mixer.music.get_busy () :
		pygame.mixer.music.load (muzyka[randrange (4)])
		pygame.mixer.music.play ()

def Gra (dwóchGraczy) :
	
	if dwóchGraczy :
		obecnyGracz = 1
	else :
		obecnyGracz = 0
	
	pygame.mixer.music.stop ()
	
	if dwóchGraczy :
		tłoGra = pygame.image.load ("Assets/Grafika/gra dwóch graczy.png")
	else :
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
			
			global zegarOpadania
			global szybkośćOpadaniaKlocka
			zegarOpadania -= 1
			if zegarOpadania == 0 :
				obecnyKlocek.Opadaj ()
				zegarOpadania = szybkośćOpadaniaKlocka
			
			for event in pygame.event.get() :
				
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
			
			klawisze = pygame.key.get_pressed ()
			
			global zegarKontrolera
			if zegarKontrolera > 0 :
				zegarKontrolera -= 1
			
			# TODO jeśli naciśnięto to pierwszy raz powinien być dłuższy cooldown
			if zegarKontrolera == 0 :
				
				if obecnyGracz == 0 and (klawisze [A1] or klawisze [A2]) or obecnyGracz == 1 and klawisze[A1] or obecnyGracz == 2 and klawisze[A2] :
					obecnyKlocek.ObróćWPrawo ()
					zegarKontrolera = 2
				elif klawisze [B1] :
					obecnyKlocek.ObróćWLewo ()
					zegarKontrolera = 2
				elif klawisze [DOWN1] :
					if not obecnyKlocek.Opadaj () :
						opadanie = False
					zegarKontrolera = 2
				
				if klawisze [RIGHT1] :
					obecnyKlocek.PrzesuńWPrawo ()
					zegarKontrolera = 2
				elif klawisze [LEFT1] :
					obecnyKlocek.PrzesuńWLewo ()
					zegarKontrolera = 2
			
			# Klocek.plansza.DebugPokażMapeKolizji (obecnyKlocek.UtwórzMacierzKolizji(obecnyKlocek.image), obecnyKlocek.x, obecnyKlocek.y)
			
			OdtwarzajMuzykę ()
			
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

def KoniecGry (dwóchGraczy) :
	
	while True :
		
		pygame.mixer.music.stop ()
		
		# TODO czy da się to uprościć?
		# czekaj 32 klatki
		for _ in range (0, 32) :
			
			pygame.display.update ()
			zegar.tick (fps)
		
		koniecGryKlatka1 = pygame.image.load ("Assets/Grafika/koniec gry klatka 1.png")
		if dwóchGraczy :
			koniecGryKlatka2 = pygame.image.load ("Assets/Grafika/koniec gry klatka 2 dwóch graczy.png")
		else :
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
	KoniecGry (dwóchGraczy)
