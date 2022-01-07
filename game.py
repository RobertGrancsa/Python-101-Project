#! /usr/bin/env python3

import pygame
from pygame.locals import *
from os import path
vec = pygame.math.Vector2

from player import Player
from blocks import LevelGen
from camera import *
from constants import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Start pygame and initialize windows
pygame.init()
pygame.display.set_caption('Untitled Game')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Directories for assets
IMG_DIR = path.join(path.dirname(__file__), 'textures')

class Game:
	def __init__(self):
		self.menuDisplay = False
		self.gameRunning = True
		self.showStatsVar = True
		self.screen = screen

		self.camera = Camera(self)
		self.follow = Follow(self.camera, self)
		self.camera.setMethod(self.follow)
		self.playerPawn = Player(vec(0, 0), self)

		self.levelGen = LevelGen(self)
		
	def setMenuDisplay(self, value):
		self.menuDisplay = value

	def getMenuDisplay(self):
		return self.menuDisplay

	def setGameRunning(self, value):
		self.gameRunning = value

	def getGameRunning(self):
		return self.gameRunning

	def getCameraOffset(self):
		return self.camera.offset

	def toggleStats(self):
		if self.showStatsVar:
			self.showStatsVar = False
		else:
			self.showStatsVar = True

	def runMenu(self):
		# Aici ar trebui sa incepi sa faci meniul
		# Sa setezi self.menuDisplay = True in constructor ca sa testezi meniul
		# folosesti functia setMenuDisplay(False) cand vrei sa inchizi meniul si sa intri in joc
		pass
	
	def run(self):
		self.playerPawn.input()
		self.levelGen.update()
		self.playerPawn.update()
		self.draw()
		
	def draw(self):
		self.deltaT = clock.tick(FPS) / 1000
		self.camera.scroll()

		if self.showStatsVar:
			display = self.levelGen.showPos()
			blockName = self.levelGen.showBlock()
			font = pygame.font.Font('freesansbold.ttf', 32)
			text = font.render("Location: " + str(display[0]), True, (255, 255, 255))
			text2 = font.render("Chunk: " + str(display[1]), True, (255, 255, 255))
			text3 = font.render("Block on: " + blockName, True, (255, 255, 255))
			screen.blit(text, (30, 30))
			screen.blit(text2, (30, 60))
			screen.blit(text3, (30, 90))

		pygame.display.update()
		clock.tick(FPS)


def main():
	game = Game()
	
	while game.getMenuDisplay():
		game.runMenu()

	while game.getGameRunning():
		game.run()

if __name__ == "__main__":
    main()
	
pygame.quit()