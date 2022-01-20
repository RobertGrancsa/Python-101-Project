#! /usr/bin/env python3

from pickle import FALSE
from time import sleep
import pygame
from pygame.locals import *
from os import path
from inventory import Inventory
vec = pygame.math.Vector2

# Initializing sound module
from pygame import mixer
mixer.init()

from player import Player
from blocks import LevelGen
from camera import *
from constants import *
from menu import Menu

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Start pygame and initialize windows
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((1920, 1080))
window = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ambiental soundtrack
mixer.music.load('audio/ambient.wav')
mixer.music.play(-1)

# Directories for assets
IMG_DIR = path.join(path.dirname(__file__), 'textures')

class Game:
	def __init__(self):
		self.menuDisplay = True
		self.gameRunning = True
		self.showStatsVar = True
		self.timer = 60.0

		self.screen = window
		self.font = pygame.font.Font('font.ttf', 32)
		self.updateTimer = self.font.render("", False, (240, 240, 240))

		self.camera = Camera(self)
		self.follow = Follow(self.camera, self)
		self.auto = Auto(self.camera, self)
		self.camera.setMethod(self.follow)

		self.playerPawn = Player(vec(0, 0), self)
		self.inventory = Inventory()

		self.levelGen = LevelGen(self)
		self.menu = Menu(self)
		
		
	def setMenuDisplay(self, value):
		if not value:
			self.camera.setMethod(self.follow)
		self.menuDisplay = value

	def getMenuDisplay(self):
		return self.menuDisplay

	def setGameRunning(self, value):
		self.gameRunning = value

	def getGameRunning(self):
		return self.gameRunning

	def getCameraOffset(self):
		return self.camera.offset

	def incrementTimer(self, add):
		self.timer += add
		self.addUpdate(add)

	def addUpdate(self, add):
		self.updateTimer = self.font.render("Added +" + str(add), True, (240, 240, 240))

	def toggleStats(self):
		if self.showStatsVar:
			self.showStatsVar = False
		else:
			self.showStatsVar = True

	def runMenu(self):
		# Aici ar trebui sa incepi sa faci meniul
		# Sa setezi self.menuDisplay = True in constructor ca sa testezi meniul
		# folosesti functia setMenuDisplay(False) cand vrei sa inchizi meniul si sa intri in joc
		self.deltaT = clock.tick(FPS) / 1000
		screen.blit(self.menu.update(), (0, 0, 1920, 1080))
		pygame.display.update()
	
	def run(self):
		# self.levelGen.collision()
		if self.timer > 0:
			self.playerPawn.input()
			self.levelGen.update()
			self.playerPawn.update()
			self.inventory.update()
			self.draw()
		else:
			end = self.font.render("GAME OVER", True, (255, 32, 32))
			end = pygame.transform.scale(end, (end.get_width() * 4, end.get_height() * 4))
			screen.blit(end, (1920 // 2 - end.get_width() // 2, 1080 // 2 - end.get_height() // 2))
			pygame.display.update()
			sleep(5)
			self.setGameRunning(False)

		
	def draw(self):
		self.deltaT = clock.tick(FPS) / 1000
		self.timer -= self.deltaT
		self.camera.scroll()

		frame = pygame.transform.scale(self.screen, (1920, 1080))
		screen.blit(frame, frame.get_rect())

		if self.showStatsVar:
			display = self.levelGen.showPos()
			blockName = self.levelGen.showBlock()
			text = self.font.render("Location: " + str(display[0]), True, (255, 255, 255))
			text2 = self.font.render("Chunk: " + str(display[1]), True, (255, 255, 255))
			text3 = self.font.render("Block on: " + blockName, True, (255, 255, 255))
			screen.blit(text, (30, 30))
			screen.blit(text2, (30, 60))
			screen.blit(text3, (30, 90))

		timer = self.font.render("Time left: " + str(int(self.timer)), True, (255, 255, 255))
		screen.blit(timer, (1920 // 2 - timer.get_width() // 2, 30))
		screen.blit(self.updateTimer, (1920 // 2 - self.updateTimer.get_width() // 2, 60))

		pygame.display.update()
		clock.tick(60)


def main():
	game = Game()
	
	while game.getMenuDisplay():
		game.runMenu()

	while game.getGameRunning():
		game.run()

if __name__ == "__main__":
    main()
	
pygame.quit()