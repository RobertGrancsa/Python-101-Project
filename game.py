#! /usr/bin/env python3

import pygame
from pygame import draw
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

# Load the texture


class Game:
	def __init__(self):
		self.menuDisplay = True
		self.screen = screen

		self.playerPawn = Player(vec(0, 0), self)
		self.camera = Camera(self)
		self.follow = Follow(self.camera, self)
		self.camera.setMethod(self.follow)

		self.levelGen = LevelGen(self)
		# screen.blit(self.background, (0, 0))
		

	def setMenuDisplay(self, value):
		self.menuDisplay = value

	def getMenuDisplay(self):
		return self.menuDisplay

	def getCameraOffset(self):
		return self.camera.offset
	
	def run(self):
		self.playerPawn.input()
		self.levelGen.update()
		self.playerPawn.update()
		self.draw()
		
	def draw(self):
		self.deltaT = clock.tick(FPS) / 1000
		self.camera.scroll()

		display = self.levelGen.showPos()
		font = pygame.font.Font('freesansbold.ttf', 32)
		text = font.render("Location: " + str(display[0]), True, (255, 255, 255))
		text2 = font.render("Chunk: " + str(display[1]), True, (255, 255, 255))
		screen.blit(text, (30, 30))
		screen.blit(text2, (30, 60))

		pygame.display.update()
		clock.tick(FPS)


def main():
	game = Game()
	
	while game.getMenuDisplay():
		game.run()

if __name__ == "__main__":
    main()
	
pygame.quit()