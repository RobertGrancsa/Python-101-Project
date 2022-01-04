import pygame
from pygame.locals import *
from constants import *
from os import path
vec = pygame.math.Vector2
IMG_DIR = path.join(path.dirname(__file__), 'textures')

class Player:
	def __init__(self, pos, game):
		self.TEXTURE_FILE = pygame.image.load(path.join(IMG_DIR, 'textures.png')).convert_alpha()
		self.pos = pos
		self.game = game
		self.playerSpeed = vec(8, 8)
		self.playerMovement = vec(0, 0)

		self.front = self.getTexture(PLAYER_FRONT)
		self.back = self.getTexture(PLAYER_BACK)

	def getPosition(self):
		return self.pos

	def getTexture(self, position):
		return self.TEXTURE_FILE.subsurface(position[0] * SIZE, position[1] * SIZE, SIZE, SIZE)

	def drawPlayer(self):
		if self.playerMovement.y > 0:
			self.game.screen.blit(self.back, (WIDTH // 2, HEIGHT // 2))
		elif self.playerMovement.y == 0:
			self.game.screen.blit(self.back, (WIDTH // 2, HEIGHT // 2))
		else:
			self.game.screen.blit(self.front, (WIDTH // 2, HEIGHT // 2))

	def update(self):
		self.pos.x += self.playerMovement.x
		self.pos.y += self.playerMovement.y
		self.drawPlayer()

	def move(self, direction):
		self.playerMovement.x = direction.x * self.playerSpeed.x
		self.playerMovement.y = direction.y * self.playerSpeed.y
		
	def input(self):
		directions = vec(0, 0)
		for event in pygame.event.get():
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					self.game.setMenuDisplay(False)
				if event.key == K_w:
					directions.y = 0
				if event.key == K_a:
					directions.x = 0
				if event.key == K_s:
					directions.y = 0
				if event.key == K_d:
					directions.x = 0
			if event.type == KEYDOWN:
				if event.key == K_w:
					directions.y += -1
				if event.key == K_a:
					directions.x += -1
				if event.key == K_s:
					directions.y += 1
				if event.key == K_d:
					directions.x += 1
			self.move(directions)