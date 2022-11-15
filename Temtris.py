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

class Temtris () :
	
	def __init__ (self) :
		
		# podstawowe ustawienia
		self.szerokośćOkna = 1024
		self.wysokośćOkna = 896
		self.zegar = None
		self.okno = None
		self.fps = 30
		
		self.PX = 4 # szerokość piksela
		self.PY = 4 # wysokość piksela
		self.X = 32 # szerokość sprite
		self.Y = 32 # wysokość sprite
		
		# kontroler NES
		
		# gracz 1
		self.A1 = K_l
		self.B1 = K_k
		self.UP1 = K_UP
		self.DOWN1 = K_DOWN
		self.LEFT1 = K_LEFT
		self.RIGHT1 = K_RIGHT
		self.START1 = K_RETURN
		self.SELECT1 = K_RSHIFT
		
		# gracz 2
		self.A2 = K_k
		self.B2 = K_l
		self.UP2 = K_UP
		self.DOWN2 = K_DOWN
		self.LEFT2 = K_LEFT
		self.RIGHT2 = K_RIGHT
		self.START2 = K_RETURN
		self.SELECT2 = K_RSHIFT
		
		# zmienne sterujące gry
		self.pauza = False
		self.poziom = 0
		self.liczbaLinii = 0
		self.liczbaLiniiCheems = 0
		self.liczbaLiniiDoge = 0
		self.liczbaLiniiBuffDoge = 0
		self.liczbaLiniiTemtris = 0
		self.liczbaPunktów = 0
		self.czasGry = 0
		self.obecnyGracz = 0
		self.zegarKontrolera = 10
		self.szybkośćOpadaniaKlocka = 60
		self.zegarOpadania = 60
		
		self.plansza = self.Plansza (self)
		
		# startujemy pygame
		pygame.init()
		pygame.mixer.init ()
		self.zegar = pygame.time.Clock ()
		self.okno = pygame.display.set_mode ((self.szerokośćOkna, self.wysokośćOkna))
		ikona = pygame.image.load("Assets/Grafika/ikona.png")
		pygame.display.set_icon(ikona)
		pygame.display.set_caption ("Temtris.py")
		
		# dźwięk i muzyka
		
		self.uderzenieSFX = pygame.mixer.Sound("Assets/Dźwięk/uderzenie.ogg")
		
		self.cheemsSFX = pygame.mixer.Sound("Assets/Dźwięk/cheems.ogg")
		self.dogeSFX = pygame.mixer.Sound("Assets/Dźwięk/doge.ogg")
		self.buffdogeSFX = pygame.mixer.Sound("Assets/Dźwięk/buffdoge.ogg")
		self.temtrisSFX = pygame.mixer.Sound("Assets/Dźwięk/temtris.ogg")
		
		self.muzyka = [
			"Assets/Dźwięk/Never Gonna Give You Up NES APU cover.ogg",
			"Assets/Dźwięk/Together Forever NES APU cover.ogg",
			"Assets/Dźwięk/Song For Denise NES APU cover.ogg",
			"Assets/Dźwięk/Szanty Bitwa NES APU cover.ogg"
		]
		
		# grafika
		self.klockiSprite = pygame.image.load ("Assets/Grafika/klocki sprite.png").convert_alpha ()
		self.fragmentySprite = pygame.image.load ("Assets/Grafika/fragmenty sprite.png").convert_alpha ()
		self.rozbijanieLiniiSprite = pygame.image.load ("Assets/Grafika/rozbijanie linii sprite.png").convert_alpha ()
		self.cyfrySprite = pygame.image.load ("Assets/Grafika/cyfry sprite.png").convert_alpha ()
		
	def Start (self) :
		
		self.Intro ()
		
		# główna pętla
		while True :
			
			dwóchGraczy = self.Menu ()
			self.Gra (dwóchGraczy)
			self.KoniecGry (dwóchGraczy)
	
	# ###########################
	#            INTRO
	# ###########################
	
	def Intro (self) :
		
		# TODO czy da się to uprościć?
		# czekaj 32 klatki
		for _ in range (0, 16) :
			for event in pygame.event.get() :
				if event.type == KEYDOWN :
					# START
					if event.key == (self.START1 or self.START2) :
						return
			
			pygame.display.update ()
			self.zegar.tick (self.fps)
		
		introSprite = pygame.image.load ("Assets/Grafika/intro sprite.png")
		
		pygame.mixer.music.load ("Assets/Dźwięk/intro.ogg")
		pygame.mixer.music.play ()
		
		for i in range (0, 4) :
			
			self.okno.blit(introSprite, Rect (6 * self.X, 11 * self.Y, 608, 320), Rect (0, i * 320, 608, 320))
			
			# czekaj 32 klatki
			for _ in range (0, 16) :
				# TODO czy da się to uprościć?
				for event in pygame.event.get() :
					if event.type == KEYDOWN :
						# START
						if event.key == (self.START1 or self.START2) :
							return
				
				pygame.display.update ()
				self.zegar.tick (self.fps)
		
		# czekaj 180 klatek
		for _ in range (0, 90) :
			for event in pygame.event.get() :
				if event.type == KEYDOWN :
					# START
					if event.key == (self.START1 or self.START2) :
						return
			
			pygame.display.update ()
			self.zegar.tick (self.fps)
			
		pygame.mixer.music.stop ()
	
	# ##########################
	#            MENU
	# ##########################
	
	class Strzałka (pygame.sprite.Sprite) :
		
			def __init__(self) :
				super().__init__()
				
				self.image = pygame.image.load ("Assets/Grafika/strzałka.png")
				self.rect = self.image.get_rect()
	
	def Menu (self) :
		
		dwóchGraczy = False
		
		# załaduj tło menu
		tłoMenu = pygame.image.load ("Assets/Grafika/menu.png")
		self.okno.blit (tłoMenu, tłoMenu.get_rect())
		
		# utwórz strzałkę wskazującą na gre dla 1 lub 2 graczy
		strzałka = self.Strzałka ()
		strzałka.rect.x = 5 * self.X - 2 * self.PX
		strzałka.rect.y = 20 * self.Y
		
		# TODO skoro jest jeden sprite to czy da się to nie robić grupą?
		wszystkieSprite = pygame.sprite.Group()
		wszystkieSprite.add (strzałka)
		wszystkieSprite.draw (self.okno)
		
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
					if event.key == (self.START1 or self.START2) :
						return dwóchGraczy
					elif event.key == (self.SELECT1 or self.SELECT2) :
						dwóchGraczy = not dwóchGraczy
						
						# narysuj tło
						self.okno.blit (tłoMenu, tłoMenu.get_rect())
						
						if dwóchGraczy :
							strzałka.rect.y += self.Y
						else :
							strzałka.rect.y -= self.Y
						
						wszystkieSprite.draw (self.okno)
			
			pygame.display.update ()
			self.zegar.tick (self.fps)
	
	# ###########################
	#             GRA
	# ###########################
	
	class Klocek (pygame.sprite.Sprite) :
		
		def __init__ (self, temtris) :
			super().__init__()
			
			self.temtris = temtris
			
			self.numerKlocka = randrange(7)
			self.obrót = 0
			
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			self.rect = self.image.get_rect ()
		
		def UstawPozycję (self, x, y) :
			
			self.x = x - 10
			self.y = y - 5
			
			self.rect.x = x * self.temtris.X
			self.rect.y = y * self.temtris.Y
			
			if self.temtris.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x, self.y) :
				return False
			else :
				return True
		
		def UtwórzGrafike (self, obrót, numerKlocka) -> pygame.Surface :
			
			grafika = pygame.Surface((128, 128)).convert_alpha ()
			grafika.blit (self.temtris.klockiSprite, Rect (0, 0, 128, 128), Rect (obrót * 128, numerKlocka * 128, 128, 128))
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
			
			if self.temtris.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x, self.y + 1) :
				return False
			else :
				self.rect.y += self.temtris.Y
				self.y += 1
				
				return True
		
		def PrzesuńWPrawo (self) :
			
			if not self.temtris.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x + 1, self.y) :
				self.rect.x += self.temtris.X
				self.x += 1
			
		def PrzesuńWLewo (self) :
			
			if not self.temtris.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x - 1, self.y) :
				self.rect.x -= self.temtris.X
				self.x -= 1
		
		def ObróćWPrawo (self) :
			
			# TODO obrót z przesunięciem
			
			obrót = (self.obrót + 1) % 4
			
			macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
			
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
			if not self.temtris.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
				self.obrót = (self.obrót + 1) % 4
				self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
		def ObróćWLewo (self) :
			
			# TODO obrót z przesunięciem
			
			obrót = (self.obrót - 1) % 4
			
			macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
			
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
			if not self.temtris.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
				self.obrót = (self.obrót - 1) % 4
				self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)

	class Fragment (pygame.sprite.Sprite) :
		
		def __init__ (self, temtris, numerFragmentu, x, y) :
			super().__init__()
			
			self.temtris = temtris
			
			self.numerFragmentu = numerFragmentu
			
			self.UstawGrafikę (0, self.numerFragmentu)
			self.rect = self.image.get_rect ()
			self.rect.x = x * self.temtris.X + 10 * self.temtris.X
			self.rect.y = y * self.temtris.Y + 5 * self.temtris.Y
			
		def UstawGrafikę (self, numerGracza, numerFragmentu) -> pygame.Surface :
			
			# numer gracza nakłada na fragment specyficzny kolor
			# jeśli numer gracza == 0 to nakłada kolor poziomu
			# jeśli nie da się osiągnąc przez nakładanie takich kolorów to zrobię spritesheeta z wszystkimi kolorami ręcznie
			
			grafika = pygame.Surface((32, 32)).convert_alpha ()
			grafika.blit (self.temtris.fragmentySprite, Rect (0, 0, 32, 32), Rect (numerFragmentu * 32, 0, 32, 32))
			grafika.set_colorkey ((0, 0, 0))
			
			self.image = grafika
			
	class Plansza () :
		
		class AnimacjaRozbijanejLinii (pygame.sprite.Sprite) :
			
			def __init__ (self, plansza, ilośćLinii, numerLinii) :
				super ().__init__ ()
				
				self.plansza = plansza
				
				self.klatka = -1
				self.ilośćLinii = ilośćLinii
				
				self.NastępnaKlatka ()
				self.rect = self.image.get_rect ()
				self.rect.x = 10 * self.plansza.temtris.X
				self.rect.y = 5 * self.plansza.temtris.Y + numerLinii * self.plansza.temtris.Y
			
			def NastępnaKlatka (self) :
				
				self.klatka += 1
				
				grafika = pygame.Surface((320, 32)).convert_alpha ()
				grafika.blit (self.plansza.temtris.rozbijanieLiniiSprite, Rect (0, 0, 320, 32), Rect ((self.ilośćLinii - 1) * 320, self.klatka * 32, 320, 32))
				grafika.set_colorkey ((0, 255, 0))
				
				self.image = grafika
		
		def __init__ (self, temtris) :
			self.temtris = temtris
			self.macierzSpriteów = [[None for x in range(10)] for y in range(20)]
			
		def Rysuj (self) :
			
			wszystkieSprite = pygame.sprite.Group ()
			
			for i in self.macierzSpriteów :
				for sprite in i :
					if sprite != None :
						wszystkieSprite.add (sprite)
			
			wszystkieSprite.draw (self.temtris.okno)
		
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
						
						self.macierzSpriteów[y + sy][x + sx] = self.temtris.Fragment (self.temtris, numerFragmentu, x + sx, y + sy)
						
			pygame.mixer.Sound.play(self.temtris.uderzenieSFX)
		
		def RozbijLinie (self, linieDoRozbicia) :
			
			# odtwórz animację
			
			spriteAnimacji = pygame.sprite.Group ()
			
			for numerLinii in linieDoRozbicia :
				spriteAnimacji.add (self.AnimacjaRozbijanejLinii (self, len (linieDoRozbicia), numerLinii))
			
			self.temtris.liczbaLinii += len (linieDoRozbicia)
			
			if len (linieDoRozbicia) == 1 :
				pygame.mixer.Sound.play(self.temtris.cheemsSFX)
				self.temtris.liczbaLiniiCheems += 1
				self.temtris.liczbaPunktów += 1
			elif len (linieDoRozbicia) == 2 :
				pygame.mixer.Sound.play(self.temtris.dogeSFX)
				self.temtris.liczbaLiniiDoge += 1
				self.temtris.liczbaPunktów += 4
			elif len (linieDoRozbicia) == 3 :
				pygame.mixer.Sound.play(self.temtris.buffdogeSFX)
				self.temtris.liczbaLiniiBuffDoge += 1
				self.temtris.liczbaPunktów += 6
			elif len (linieDoRozbicia) == 4 :
				pygame.mixer.Sound.play(self.temtris.temtrisSFX)
				self.temtris.liczbaLiniiTemtris += 1
				self.temtris.liczbaPunktów += 8
			
			for x in range (0, 32) :
				
				spriteAnimacji.draw (self.temtris.okno)
				
				pygame.display.update ()
				self.temtris.zegar.tick (self.temtris.fps * 2)
				
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
						self.macierzSpriteów [y][x].rect.y = y * self.temtris.Y + 5 * self.temtris.Y

	def OdtwarzajMuzykę (self) :
		
		if not pygame.mixer.music.get_busy () :
			pygame.mixer.music.load (self.muzyka[randrange (4)])
			pygame.mixer.music.play ()

	def Gra (self, dwóchGraczy) :
		
		pygame.mixer.music.stop ()
		
		licznikLinii = []
		licznikPunktów = []
		
		licznikLinii.append (self.Liczba (self, 4, 3, 9))
		licznikPunktów.append (self.Liczba (self, 4, 3, 12))
		
		if dwóchGraczy :
			tłoGra = pygame.image.load ("Assets/Grafika/gra dwóch graczy.png")
			licznikLinii.append (self.Liczba (self, 4, 2, 2))
			licznikPunktów.append (self.Liczba (self, 4, 4, 4))
		else :
			tłoGra = pygame.image.load ("Assets/Grafika/gra.png")
			
		self.okno.blit (tłoGra, tłoGra.get_rect())
		
		następnyKolcek = self.Klocek (self)
		następnyKolcek.UstawPozycję (4, 4)
		
		while True :
			
			# stwórz obecny i następny klocek
			
			obecnyKlocek = następnyKolcek
			if not obecnyKlocek.UstawPozycję (13, 5) :
				break
			następnyKolcek = self.Klocek (self)
			następnyKolcek.UstawPozycję (4, 4)
			
			wszystkieSprite = pygame.sprite.Group()
			wszystkieSprite.add (obecnyKlocek)
			wszystkieSprite.add (następnyKolcek)
			wszystkieSprite.draw (self.okno)
			
			# opadanie klocka
			
			while True :
				
				self.zegarOpadania -= 1
				if self.zegarOpadania == 0 :
					obecnyKlocek.Opadaj ()
					self.zegarOpadania = self.szybkośćOpadaniaKlocka
				
				for event in pygame.event.get() :
					
					# naciśnięcie X na oknie
					if event.type == QUIT:
						pygame.quit ()
						exit ()
				
				klawisze = pygame.key.get_pressed ()
				
				if self.zegarKontrolera > 0 :
					self.zegarKontrolera -= 1
				
				# TODO jeśli naciśnięto to pierwszy raz powinien być dłuższy cooldown
				if self.zegarKontrolera == 0 :
					
					if self.obecnyGracz == 0 and klawisze[self.A1] or self.obecnyGracz == 1 and klawisze[self.A2] :
						obecnyKlocek.ObróćWPrawo ()
						self.zegarKontrolera = 2
					elif self.obecnyGracz == 0 and klawisze[self.B1] or self.obecnyGracz == 1 and klawisze[self.B2] :
						obecnyKlocek.ObróćWLewo ()
						self.zegarKontrolera = 2
					elif self.obecnyGracz == 0 and klawisze[self.DOWN1] or self.obecnyGracz == 1 and klawisze[self.DOWN2] :
						if not obecnyKlocek.Opadaj () :
							break
						self.zegarKontrolera = 2
					
					if self.obecnyGracz == 0 and klawisze[self.RIGHT1] or self.obecnyGracz == 1 and klawisze[self.RIGHT2] :
						obecnyKlocek.PrzesuńWPrawo ()
						self.zegarKontrolera = 2
					elif self.obecnyGracz == 0 and klawisze[self.LEFT1] or self.obecnyGracz == 1 and klawisze[self.LEFT2] :
						obecnyKlocek.PrzesuńWLewo ()
						self.zegarKontrolera = 2
				
				self.OdtwarzajMuzykę ()
				
				self.okno.blit (tłoGra, tłoGra.get_rect())
				wszystkieSprite.draw (self.okno)
				self.plansza.Rysuj ()
					
				for licznik in licznikLinii :
					licznik.Rysuj ()
				for licznik in licznikPunktów :
					licznik.Rysuj ()
					
				pygame.display.update ()
				self.zegar.tick (self.fps)
			
			# umieszczanie klocka
			self.plansza.UmieśćKlocek (obecnyKlocek.UtwórzMacierzKolizji (obecnyKlocek.image), obecnyKlocek.x, obecnyKlocek.y)
			
			# sprawdzanie linii
			linieDoRozbicia = self.plansza.SprawdźRozbicieLinii ()
			
			if len (linieDoRozbicia) > 0 :
				self.plansza.RozbijLinie (linieDoRozbicia)
				licznikLinii[0].Ustaw (self.liczbaLinii)
				licznikPunktów[0].Ustaw (self.liczbaPunktów)
				
			# odśwież ekran
			self.okno.blit (tłoGra, tłoGra.get_rect())
			wszystkieSprite.draw (self.okno)
			self.plansza.Rysuj ()
			
			for licznik in licznikLinii :
				licznik.Rysuj ()
			for licznik in licznikPunktów :
				licznik.Rysuj ()
				
			pygame.display.update ()
			self.zegar.tick (self.fps)

	# ###########################
	#         KONIEC GRY
	# ###########################
	
	def KoniecGry (self, dwóchGraczy) :
		
		while True :
			
			pygame.mixer.music.stop ()
			
			# TODO czy da się to uprościć?
			# czekaj 32 klatki
			for _ in range (0, 32) :
				
				pygame.display.update ()
				self.zegar.tick (self.fps)
			
			koniecGryKlatka1 = pygame.image.load ("Assets/Grafika/koniec gry klatka 1.png")
			if dwóchGraczy :
				koniecGryKlatka2 = pygame.image.load ("Assets/Grafika/koniec gry klatka 2 dwóch graczy.png")
			else :
				koniecGryKlatka2 = pygame.image.load ("Assets/Grafika/koniec gry klatka 2.png")
			
			pygame.mixer.music.load ("Assets/Dźwięk/koniec gry.ogg")
			pygame.mixer.music.play ()
			
			self.okno.blit (koniecGryKlatka1, koniecGryKlatka1.get_rect())
			pygame.display.update ()
			self.zegar.tick (self.fps)
			
			for _ in range (0, 42) :
				
				pygame.display.update ()
				self.zegar.tick (self.fps)
			
			self.okno.blit (koniecGryKlatka2, koniecGryKlatka2.get_rect())
			pygame.display.update ()
			self.zegar.tick (self.fps)
			
			while True :
			
				for event in pygame.event.get() :
					# naciśnięcie X na oknie
					if event.type == QUIT:
						pygame.quit ()
						exit ()
						
					if event.type == KEYDOWN :
						if event.key == (self.START1 or self.START2) :
							return
				
				pygame.display.update ()
				self.zegar.tick (self.fps)
	
	# #######################
	#        LICZNIKI
	# #######################
	
	class Liczba () :
		
		def __init__ (self, temtris, długość, x, y) :
			
			self.temtris = temtris
			
			self.cyfry = []
			self.liczba = 0
			
			for i in range (0, długość) :
				self.cyfry.append (self.Cyfra (self.temtris, x + długość - i, y))
			
		def Ustaw (self, liczba) :
			
			self.liczba = liczba
			
			liczba = self.liczba
			for cyfra in self.cyfry :
				cyfra.Ustaw (liczba % 10)
				liczba = liczba // 10
			
		def Rysuj (self) :
			
			cyfry = pygame.sprite.Group ()
			
			for cyfra in self.cyfry :
				cyfry.add (cyfra)
				
			cyfry.draw (self.temtris.okno)
			
		class Cyfra (pygame.sprite.Sprite) :
		
			def __init__ (self, temtris, x, y) :
				super ().__init__ ()
				
				self.temtris = temtris
				self.Ustaw (0)
				self.rect = self.image.get_rect ()
				self.rect.x = x * self.temtris.X
				self.rect.y = y * self.temtris.Y
				
			def Ustaw (self, cyfra) :
				
				grafika = pygame.Surface((32, 32)).convert_alpha ()
				grafika.blit (self.temtris.cyfrySprite, Rect (0, 0, 32, 32), Rect (cyfra * 32, 0, 32, 32))
				grafika.set_colorkey ((0, 0, 0))
				self.image = grafika

def Main () :
	temtris = Temtris ()
	temtris.Start ()

if __name__ == "__main__" :
	Main ()
