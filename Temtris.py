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
		self.fps = 60
		
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
		self.A2 = K_l
		self.B2 = K_k
		self.UP2 = K_UP
		self.DOWN2 = K_DOWN
		self.LEFT2 = K_LEFT
		self.RIGHT2 = K_RIGHT
		self.START2 = K_RETURN
		self.SELECT2 = K_RSHIFT
		
		# zmienne sterujące gry
		self.pauza = False
		self.poziom = 0
		self.liczbaLinii = [0, 0]
		self.liczbaLiniiCheems = [0, 0]
		self.liczbaLiniiDoge = [0, 0]
		self.liczbaLiniiBuffDoge = [0, 0]
		self.liczbaLiniiTemtris = [0, 0]
		self.liczbaPunktów = [0, 0]
		self.czasGry = 0
		self.dwóchGraczy = False
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
		self.uderzenieSFX = pygame.mixer.Sound("Assets/Dzwiek/uderzenie.ogg")
		
		self.cheemsSFX = pygame.mixer.Sound("Assets/Dzwiek/cheems.ogg")
		self.dogeSFX = pygame.mixer.Sound("Assets/Dzwiek/doge.ogg")
		self.buffdogeSFX = pygame.mixer.Sound("Assets/Dzwiek/buffdoge.ogg")
		self.temtrisSFX = pygame.mixer.Sound("Assets/Dzwiek/temtris.ogg")
		
		self.muzyka = [
			"Assets/Dzwiek/Never Gonna Give You Up NES APU cover.ogg",
			"Assets/Dzwiek/Together Forever NES APU cover.ogg",
			"Assets/Dzwiek/Song For Denise NES APU cover.ogg",
			"Assets/Dzwiek/Szanty Bitwa NES APU cover.ogg"
		]
		
		# grafika
		self.tłoMenu = pygame.image.load ("Assets/Grafika/menu.png")
		self.tłoGra = pygame.image.load ("Assets/Grafika/gra.png")
		self.tłoGra2Graczy = pygame.image.load ("Assets/Grafika/gra dwoch graczy.png")
		self.koniecGryKlatka1 = pygame.image.load ("Assets/Grafika/koniec gry klatka 1.png")
		self.koniecGryKlatka2 = pygame.image.load ("Assets/Grafika/koniec gry klatka 2.png")
		self.koniecGryKlatka2dwochGraczy = pygame.image.load ("Assets/Grafika/koniec gry klatka 2 dwoch graczy.png")
		
		self.introSprite = pygame.image.load ("Assets/Grafika/intro sprite.png")
		self.strzałkaSprite = pygame.image.load ("Assets/Grafika/strzalka.png")
		self.klockiSprite = pygame.image.load ("Assets/Grafika/klocki sprite.png").convert_alpha ()
		self.klockiSpriteGracz1 = pygame.image.load ("Assets/Grafika/klocki sprite gracz 1.png").convert_alpha ()
		self.klockiSpriteGracz2 = pygame.image.load ("Assets/Grafika/klocki sprite gracz 2.png").convert_alpha ()
		self.fragmentySprite = pygame.image.load ("Assets/Grafika/fragmenty sprite.png").convert_alpha ()
		self.rozbijanieLiniiSprite = pygame.image.load ("Assets/Grafika/rozbijanie linii sprite.png").convert_alpha ()
		self.cyfrySprite = pygame.image.load ("Assets/Grafika/cyfry sprite.png").convert_alpha ()
		
		self.pauzaSprite = pygame.image.load ("Assets/Grafika/pauza.png").convert_alpha ()
		self.czaszkaSprite = pygame.image.load ("Assets/Grafika/czaszka.png").convert_alpha ()
		self.koronaSprite = pygame.image.load ("Assets/Grafika/korona.png").convert_alpha ()
		
	def Start (self) :
		
		self.Intro ()
		
		# główna pętla
		while True :
			
			self.Menu ()
			self.Gra ()
			self.KoniecGry ()
	
	# ###########################
	#            INTRO
	# ###########################
	
	def Intro (self) :
		
		if not self.CzekajLubPomiń (32) :
			return
		
		pygame.mixer.music.load ("Assets/Dzwiek/intro.ogg")
		pygame.mixer.music.play ()
		
		for i in range (0, 4) :
			
			# rysuj na ekranie logo
			self.okno.blit(self.introSprite, Rect (6 * self.X, 11 * self.Y, 608, 320), Rect (0, i * 320, 608, 320))
			
			if not self.CzekajLubPomiń (32) :
				return
		
		if not self.CzekajLubPomiń (180) :
			return
			
		pygame.mixer.music.stop ()
	
	# ##########################
	#            MENU
	# ##########################
	
	class Strzałka (pygame.sprite.Sprite) :
		"""Reprezentuje sprite strzałki w menu, służącej do wyboru trybu gry"""
		
		def __init__(self, temtris, x, y) :
			super().__init__()
			
			self.image = temtris.strzałkaSprite
			self.rect = self.image.get_rect()
			self.rect.x = x * temtris.X - 2 * temtris.PX
			self.rect.y = y * temtris.Y
	
	def Menu (self) :
		
		# wyzeruj zmienne sterujące grą
		self.pauza = False
		self.poziom = 0
		self.liczbaLinii = [0, 0]
		self.liczbaLiniiCheems = [0, 0]
		self.liczbaLiniiDoge = [0, 0]
		self.liczbaLiniiBuffDoge = [0, 0]
		self.liczbaLiniiTemtris = [0, 0]
		self.liczbaPunktów = [0, 0]
		self.czasGry = 0
		self.dwóchGraczy = False
		self.obecnyGracz = 0
		self.zegarKontrolera = 10
		self.szybkośćOpadaniaKlocka = 60
		self.zegarOpadania = 60
		
		self.plansza = self.Plansza (self)
		
		# załaduj tło menu
		self.okno.blit (self.tłoMenu, self.tłoMenu.get_rect())
		
		# utwórz strzałkę wskazującą na gre dla 1 lub 2 graczy
		strzałka = self.Strzałka (self, 5, 20)
		
		wszystkieSprite = pygame.sprite.Group()
		wszystkieSprite.add (strzałka)
		wszystkieSprite.draw (self.okno)
		
		# odtwarzaj muzykę w menu
		pygame.mixer.music.load ("Assets/Dzwiek/temtris theme.ogg")
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
						return
					elif event.key == (self.SELECT1 or self.SELECT2) :
						self.dwóchGraczy = not self.dwóchGraczy
						
						# narysuj tło
						self.okno.blit (self.tłoMenu, self.tłoMenu.get_rect())
						
						if self.dwóchGraczy :
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
		"""Reprezentuje klocek nad którym gracz ma kontrolę"""
		
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
			
			spritesheet = self.temtris.klockiSprite
			
			if self.temtris.dwóchGraczy :
				if self.temtris.obecnyGracz == 0 :
					spritesheet = self.temtris.klockiSpriteGracz1
				else :
					spritesheet = self.temtris.klockiSpriteGracz2
			
			grafika = pygame.Surface((128, 128)).convert_alpha ()
			grafika.blit (spritesheet, Rect (0, 0, 128, 128), Rect (obrót * 128, numerKlocka * 128, 128, 128))
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
				self.y += 1
				self.rect.y += self.temtris.Y
				
				return True
		
		def PrzesuńWPrawo (self) :
			
			if not self.temtris.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x + 1, self.y) :
				self.x += 1
				self.rect.x += self.temtris.X
			
		def PrzesuńWLewo (self) :
			
			if not self.temtris.plansza.SprawdźKolizję (self.UtwórzMacierzKolizji (self.image), self.x - 1, self.y) :
				self.x -= 1
				self.rect.x -= self.temtris.X
		
		def ObróćWPrawo (self) :
			
			obrót = (self.obrót + 1) % 4
			macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
			if not self.temtris.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
				self.obrót = (self.obrót + 1) % 4
				self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			else :
				# obrót z przesunięciem
				if not self.temtris.plansza.SprawdźKolizję (macierzKolizji, self.x - 1, self.y) :
					self.x -= 1
					self.rect.x -= self.temtris.X
					self.obrót = (self.obrót + 1) % 4
					self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
		def ObróćWLewo (self) :
			
			obrót = (self.obrót - 1) % 4
			macierzKolizji = self.UtwórzMacierzKolizji (self.UtwórzGrafike (obrót, self.numerKlocka))
			self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
			if not self.temtris.plansza.SprawdźKolizję (macierzKolizji, self.x, self.y) :
				self.obrót = (self.obrót - 1) % 4
				self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			else :
				# obrót z przesunięciem
				if not self.temtris.plansza.SprawdźKolizję (macierzKolizji, self.x + 1, self.y) :
					self.x += 1
					self.rect.x += self.temtris.X
					self.obrót = (self.obrót - 1) % 4
					self.image = self.UtwórzGrafike (self.obrót, self.numerKlocka)
			
	class Plansza () :
		"""Reprezentuje plansze, na której rozgrywa się gra"""
		
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
		
		def Odśwież (self) :
			for i in self.macierzSpriteów :
				for sprite in i :
					if sprite != None :
						sprite.UstawGrafikę (sprite.numerFragmentu)
		
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
						
						self.macierzSpriteów[y + sy][x + sx] = self.Fragment (self.temtris, numerFragmentu, x + sx, y + sy)
						
			pygame.mixer.Sound.play(self.temtris.uderzenieSFX)
		
		def RozbijLinie (self, linieDoRozbicia) :
			
			# utwórz sprite animacji
			spriteAnimacji = pygame.sprite.Group ()
			
			for numerLinii in linieDoRozbicia :
				spriteAnimacji.add (self.AnimacjaRozbijanejLinii (self, len (linieDoRozbicia), numerLinii))
			
			# podlicz punkty i statystykę
			self.temtris.liczbaLinii[self.temtris.obecnyGracz] += len (linieDoRozbicia)
			
			if len (linieDoRozbicia) == 1 :
				pygame.mixer.Sound.play(self.temtris.cheemsSFX)
				self.temtris.liczbaLiniiCheems[self.temtris.obecnyGracz] += 1
				self.temtris.liczbaPunktów[self.temtris.obecnyGracz] += 1
			elif len (linieDoRozbicia) == 2 :
				pygame.mixer.Sound.play(self.temtris.dogeSFX)
				self.temtris.liczbaLiniiDoge[self.temtris.obecnyGracz] += 1
				self.temtris.liczbaPunktów[self.temtris.obecnyGracz] += 4
			elif len (linieDoRozbicia) == 3 :
				pygame.mixer.Sound.play(self.temtris.buffdogeSFX)
				self.temtris.liczbaLiniiBuffDoge[self.temtris.obecnyGracz] += 1
				self.temtris.liczbaPunktów[self.temtris.obecnyGracz] += 6
			elif len (linieDoRozbicia) == 4 :
				pygame.mixer.Sound.play(self.temtris.temtrisSFX)
				self.temtris.liczbaLiniiTemtris[self.temtris.obecnyGracz] += 1
				self.temtris.liczbaPunktów[self.temtris.obecnyGracz] += 8
			
			# odtwórz animację
			for x in range (0, 32) :
				
				spriteAnimacji.draw (self.temtris.okno)
				
				pygame.display.update ()
				self.temtris.zegar.tick (self.temtris.fps)
				
				for sprite in spriteAnimacji :
					sprite.NastępnaKlatka ()
			
			# zmień grafiki
			
			for numerLinii in linieDoRozbicia :
				if numerLinii - 1 >= 0 :
					for x in range (0, 10) :
						if self.macierzSpriteów [numerLinii - 1][x] != None :
							self.macierzSpriteów[numerLinii - 1][x].UstawGrafikę (self.macierzSpriteów[numerLinii - 1][x].numerFragmentu & 13)
				
				if numerLinii + 1 < 20 :
					for x in range (0, 10) :
						if self.macierzSpriteów [numerLinii + 1][x] != None :
							self.macierzSpriteów[numerLinii + 1][x].UstawGrafikę (self.macierzSpriteów[numerLinii + 1][x].numerFragmentu & 7)
			
			# usuń linie i utwórz nowe na górze
			for numerLinii in linieDoRozbicia :
				del self.macierzSpriteów [numerLinii]
				self.macierzSpriteów.insert (0, [])
				for _ in range (0, 10) :
					self.macierzSpriteów[0].append (None)
			
			# odśwież pozycje fragmentów
			for y in range (0, 20) :
				for x in range (0, 10) :
					if self.macierzSpriteów [y][x] != None :
						self.macierzSpriteów [y][x].rect.y = y * self.temtris.Y + 5 * self.temtris.Y
		
		class Fragment (pygame.sprite.Sprite) :
			"""Reprezentuje pojedynczy mały fragment klocka położony na planszy"""
			
			def __init__ (self, temtris, numerFragmentu, x, y) :
				super().__init__()
				
				self.temtris = temtris
				self.numerGracza = self.temtris.obecnyGracz
				
				self.numerFragmentu = numerFragmentu
				
				self.UstawGrafikę (self.numerFragmentu)
				self.rect = self.image.get_rect ()
				self.rect.x = x * self.temtris.X + 10 * self.temtris.X
				self.rect.y = y * self.temtris.Y + 5 * self.temtris.Y
				
			def UstawGrafikę (self, numerFragmentu) -> pygame.Surface :
				
				numerKoloru = self.temtris.poziom
				
				if self.temtris.dwóchGraczy :
					if self.numerGracza == 0 :
						numerKoloru = 7
					else :
						numerKoloru = 3
				
				grafika = pygame.Surface((32, 32)).convert_alpha ()
				grafika.blit (self.temtris.fragmentySprite, Rect (0, 0, 32, 32), Rect (numerFragmentu * 32, numerKoloru * 32, 32, 32))
				grafika.set_colorkey ((0, 0, 0))
				
				self.image = grafika
						
		class AnimacjaRozbijanejLinii (pygame.sprite.Sprite) :
			"""Reprezentuje pojedynczy animowany pasek podczas rozbijania linii"""
			
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
	
	class Pauza (pygame.sprite.Sprite) :
		"""Tekst wyświetlany na ekranie podczas trwania pauzy"""
		
		def __init__ (self, temtris, x, y) :
			super ().__init__ ()
			
			grafika = pygame.Surface((192, 32)).convert_alpha ()
			grafika.blit (temtris.pauzaSprite, Rect (0, 0, 192, 32), Rect (0, 0, 192, 32))
			grafika.set_colorkey ((0, 0, 0))
			
			self.image = grafika
			self.rect = self.image.get_rect ()
			self.rect.x = x * temtris.X
			self.rect.y = y * temtris.Y
	
	def Pauza (self) :
		
		self.mixer.music.Pause ()
		pauza = self.Pauza (4, 4)
		
		self.pauza = True
		while self.pauza :
			for event in pygame.event.get() :
						
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
				
				if event.type == KEYDOWN :
					if event.key == (self.START1 or self.START2) :
						self.pauza = False
			
			pygame.display.update ()
			self.zegar.tick (self.fps)
		
		self.mixer.music.Resume ()
		
	def OdtwarzajMuzykę (self) :
		
		if not pygame.mixer.music.get_busy () :
			pygame.mixer.music.load (self.muzyka[randrange (4)])
			pygame.mixer.music.play ()
		
	def NastępnaMelodia (self) :
		
		pygame.mixer.music.stop ()
		pygame.mixer.music.load (self.muzyka[randrange (4)])
		pygame.mixer.music.play ()
	
	def NastępnyPoziom (self) :
		if self.szybkośćOpadaniaKlocka > 4 :
			self.szybkośćOpadaniaKlocka -= 4
		if self.poziom < 15 :
			self.poziom += 1
		self.plansza.Odśwież ()
	
	def Gra (self) :
		
		pygame.mixer.music.stop ()
		
		licznikLinii = []
		licznikPunktów = []
		
		licznikLinii.append (self.Liczba (self, 4, 3, 9))
		licznikPunktów.append (self.Liczba (self, 4, 3, 12))
		
		następnyKolcek = []
		następnyKolcek.append (self.Klocek (self))
		następnyKolcek[0].UstawPozycję (4, 4)
		
		if self.dwóchGraczy :
			
			tłoGra = self.tłoGra2Graczy
			
			self.obecnyGracz = 1
			
			licznikLinii.append (self.Liczba (self, 4, 21, 9))
			licznikPunktów.append (self.Liczba (self, 4, 21, 12))
			
			następnyKolcek.append (self.Klocek (self))
			następnyKolcek[1].UstawPozycję (22, 4)
			
			self.obecnyGracz = 0
		else :
			tłoGra = self.tłoGra
		
		self.okno.blit (tłoGra, tłoGra.get_rect())
		
		while True :
			
			# stwórz obecny i następny klocek
			obecnyKlocek = następnyKolcek[self.obecnyGracz]
			if not obecnyKlocek.UstawPozycję (13, 5) :
				break
			następnyKolcek[self.obecnyGracz] = self.Klocek (self)
			if self.obecnyGracz == 0 :
				następnyKolcek[self.obecnyGracz].UstawPozycję (4, 4)
			else :
				następnyKolcek[self.obecnyGracz].UstawPozycję (22, 4)
			
			wszystkieSprite = pygame.sprite.Group()
			wszystkieSprite.add (obecnyKlocek)
			wszystkieSprite.add (następnyKolcek[0])
			if self.dwóchGraczy :
				wszystkieSprite.add (następnyKolcek[1])
			wszystkieSprite.draw (self.okno)
			
			# opadanie klocka
			
			while True :
				
				self.zegarOpadania -= 1
				if self.zegarOpadania == 0 :
					if not obecnyKlocek.Opadaj () :
						break
					self.zegarOpadania = self.szybkośćOpadaniaKlocka
				
				for event in pygame.event.get() :
					
					# naciśnięcie X na oknie
					if event.type == QUIT:
						pygame.quit ()
						exit ()
					
					if event.type == KEYDOWN:
						if event.key == (self.SELECT1 or self.SELECT2) :
							self.NastępnaMelodia ()
						if event.key == (self.START1 or self.START2) :
							self.Pauza ()
				
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
				
				# policz klatkę czasu gry
				self.czasGry += 1
				
				pygame.display.update ()
				self.zegar.tick (self.fps)
			
			# umieszczanie klocka
			self.plansza.UmieśćKlocek (obecnyKlocek.UtwórzMacierzKolizji (obecnyKlocek.image), obecnyKlocek.x, obecnyKlocek.y)
			
			# sprawdzanie linii
			linieDoRozbicia = self.plansza.SprawdźRozbicieLinii ()
			
			if len (linieDoRozbicia) > 0 :
				
				if self.dwóchGraczy :
					if self.liczbaLinii[0] % 30 + len (linieDoRozbicia) >= 30 :
						self.NastępnyPoziom ()
				else :
					if (self.liczbaLinii[0] + self.liczbaLinii[1]) % 30 + len (linieDoRozbicia) >= 30 :
						self.NastępnyPoziom ()
				
				self.plansza.RozbijLinie (linieDoRozbicia)
				licznikLinii[self.obecnyGracz].Ustaw (self.liczbaLinii[self.obecnyGracz])
				licznikPunktów[self.obecnyGracz].Ustaw (self.liczbaPunktów[self.obecnyGracz])
			
			# policz klatkę czasu gry
			self.czasGry += 1
			
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
			
			# zmień gracza
			if self.dwóchGraczy :
				self.obecnyGracz = 1 - self.obecnyGracz
			

	# ###########################
	#         KONIEC GRY
	# ###########################
	
	class Korona (pygame.sprite.Sprite) :
		"""Prosta ikonka w ekranie końca gry dla dwóch graczy, wyświetlana jest przy graczu z większą ilością punktów"""
		
		def __init__ (self, temtris, x, y) :
			super ().__init__ ()
			
			grafika = pygame.Surface((32, 32)).convert_alpha ()
			grafika.blit (temtris.koronaSprite, Rect (0, 0, 32, 32), Rect (0, 0, 32, 32))
			grafika.set_colorkey ((0, 0, 0))
			
			self.image = grafika
			self.rect = self.image.get_rect ()
			self.rect.x = x * temtris.X
			self.rect.y = y * temtris.Y
	
	class Czaszka (pygame.sprite.Sprite) :
		"""Prosta ikonka w ekranie końca gry dla dwóch graczy, wyświetlana jest przy graczu, którego następny klocek nie zmieścił się już na planszy"""
		
		def __init__ (self, temtris, x, y) :
			super ().__init__ ()
			
			grafika = pygame.Surface((32, 32)).convert_alpha ()
			grafika.blit (temtris.czaszkaSprite, Rect (0, 0, 32, 32), Rect (0, 0, 32, 32))
			grafika.set_colorkey ((0, 0, 0))
			
			self.image = grafika
			self.rect = self.image.get_rect ()
			self.rect.x = x * temtris.X
			self.rect.y = y * temtris.Y
	
	def KoniecGry (self) :
		
		while True :
			
			pygame.mixer.music.stop ()
			
			self.Czekaj (64)
			
			if self.dwóchGraczy :
				koniecGryKlatka2 = self.koniecGryKlatka2dwochGraczy
			else :
				koniecGryKlatka2 = self.koniecGryKlatka2
			
			pygame.mixer.music.load ("Assets/Dzwiek/koniec gry.ogg")
			pygame.mixer.music.play ()
			
			self.okno.blit (self.koniecGryKlatka1, self.koniecGryKlatka1.get_rect())
			pygame.display.update ()
			self.zegar.tick (self.fps)
			
			self.Czekaj (84)
			
			self.okno.blit (koniecGryKlatka2, koniecGryKlatka2.get_rect())
			pygame.display.update ()
			self.zegar.tick (self.fps)
			
			liczniki = []
			
			ikony = pygame.sprite.Group ()
			
			# statystyki gracza 1
			
			pozycjaX = 10
			if self.dwóchGraczy :
				pozycjaX = 6
			
			for i in range (13, 25, 2) :
				liczniki.append (self.Liczba (self, 4, pozycjaX, i))
			
			liczniki[0].Ustaw (self.liczbaPunktów[0])
			liczniki[1].Ustaw (self.liczbaLinii[0])
			liczniki[2].Ustaw (self.liczbaLiniiCheems[0])
			liczniki[3].Ustaw (self.liczbaLiniiDoge[0])
			liczniki[4].Ustaw (self.liczbaLiniiBuffDoge[0])
			liczniki[5].Ustaw (self.liczbaLiniiTemtris[0])
			
			# czas gry
			liczniki.append (self.Liczba (self, 3, 10, 25))
			liczniki.append (self.Liczba (self, 2, 14, 25))
			liczniki[7].Ustaw (self.czasGry // 3600)
			liczniki[6].Ustaw (self.czasGry // 60 % 60)
			
			# statystyki gracza 2
			if self.dwóchGraczy :
				for i in range (13, 25, 2) :
					liczniki.append (self.Liczba (self, 4, 11, i))
				
				liczniki[8].Ustaw (self.liczbaPunktów[1])
				liczniki[9].Ustaw (self.liczbaLinii[1])
				liczniki[10].Ustaw (self.liczbaLiniiCheems[1])
				liczniki[11].Ustaw (self.liczbaLiniiDoge[1])
				liczniki[12].Ustaw (self.liczbaLiniiBuffDoge[1])
				liczniki[13].Ustaw (self.liczbaLiniiTemtris[1])
				
				if self.liczbaPunktów[0] != self.liczbaPunktów[1] :
					if self.liczbaPunktów[0] > self.liczbaPunktów[1] :
						ikony.add (self.Korona (self, 7, 11))
					else :
						ikony.add (self.Korona (self, 12, 11))
				
				if self.obecnyGracz == 0 :
					ikony.add (self.Czaszka (self, 10, 11))
				else :
					ikony.add (self.Czaszka (self, 15, 11))
			
			while True :
			
				for licznik in liczniki :
					licznik.Rysuj ()
				ikony.draw (self.okno)
				
				pygame.display.update ()
				self.zegar.tick (self.fps)
			
				for event in pygame.event.get() :
					# naciśnięcie X na oknie
					if event.type == QUIT:
						pygame.quit ()
						exit ()
						
					if event.type == KEYDOWN :
						if event.key == (self.START1 or self.START2) :
							return
				
	# #######################
	#       PRZYDATNE
	# #######################
	
	def Czekaj (self, klatki) :
		for _ in range (0, klatki) :
			
			for event in pygame.event.get() :
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
					
			pygame.display.update ()
			self.zegar.tick (self.fps)
	
	def CzekajLubPomiń (self, klatki) :
		for _ in range (0, klatki) :
			for event in pygame.event.get() :
				
				# naciśnięcie X na oknie
				if event.type == QUIT:
					pygame.quit ()
					exit ()
					
				if event.type == KEYDOWN :
					# START
					if event.key == (self.START1 or self.START2) :
						return False
			
			pygame.display.update ()
			self.zegar.tick (self.fps)
		
		return True
	
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
