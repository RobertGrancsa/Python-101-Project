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
		self.directions = vec(0, 0)
		self.lookingAt = SOUTH

		self.front = self.getTexture(PLAYER_FRONT)
		self.back = self.getTexture(PLAYER_BACK)
		self.left = self.getTexture(PLAYER_LEFT)
		self.right = self.getTexture(PLAYER_RIGHT)

	def getPosition(self):
		return self.pos

	def getTexture(self, position):
		return self.TEXTURE_FILE.subsurface(position[0] * SIZE, position[1] * SIZE, SIZE, SIZE)

	def drawPlayer(self):
		if self.playerMovement.y < 0:
			self.game.screen.blit(self.back, (WIDTH // 2, HEIGHT // 2))
		elif self.playerMovement.y > 0:
			self.game.screen.blit(self.front, (WIDTH // 2, HEIGHT // 2))
		elif self.playerMovement.x < 0:
			self.game.screen.blit(self.right, (WIDTH // 2, HEIGHT // 2))
		elif self.playerMovement.x > 0:
			self.game.screen.blit(self.left, (WIDTH // 2, HEIGHT // 2))
		else:
			if self.lookingAt == NORTH:
				self.game.screen.blit(self.back, (WIDTH // 2, HEIGHT // 2))
			if self.lookingAt == SOUTH:
				self.game.screen.blit(self.front, (WIDTH // 2, HEIGHT // 2))
			if self.lookingAt == WEST:
				self.game.screen.blit(self.left, (WIDTH // 2, HEIGHT // 2))
			if self.lookingAt == EAST:
				self.game.screen.blit(self.right, (WIDTH // 2, HEIGHT // 2))

		

	def update(self):
		self.move()
		self.drawPlayer()

	def move(self):
		self.playerMovement.x = self.directions.x * self.playerSpeed.x
		self.playerMovement.y = self.directions.y * self.playerSpeed.y

		self.pos.x += self.playerMovement.x
		self.pos.y += self.playerMovement.y
		
	def input(self):
		for event in pygame.event.get():
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					self.game.setMenuDisplay(False)
				if event.key == K_w:
					self.directions.y = 0
					self.lookingAt = NORTH
				if event.key == K_a:
					self.directions.x = 0
					self.lookingAt = WEST
				if event.key == K_s:
					self.directions.y = 0
					self.lookingAt = SOUTH
				if event.key == K_d:
					self.directions.x = 0
					self.lookingAt = EAST
			if event.type == KEYDOWN:
				if event.key == K_w:
					self.directions.y += -1
				if event.key == K_a:
					self.directions.x += -1
				if event.key == K_s:
					self.directions.y += 1
				if event.key == K_d:
					self.directions.x += 1
				if event.key == K_SPACE:
					self.game.levelGen.getBlock(self.lookingAt)
				if event.key == K_f:
					self.game.levelGen.placeBlock(self.lookingAt)
			