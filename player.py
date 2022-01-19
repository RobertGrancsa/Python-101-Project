import pygame
from pygame.locals import *
from constants import *
from os import path
vec = pygame.math.Vector2
IMG_DIR = path.join(path.dirname(__file__), 'textures')

# Initializing block sound effects (used in playSound function below)
from pygame import mixer
grassSound = mixer.Sound('audio/grass.wav')
sandSound = mixer.Sound('audio/sand.wav')
waterSound = mixer.Sound('audio/water.wav')

# Initializing block placing sound effects (used at F key-binding)
blockSound = mixer.Sound('audio/place_block.wav')

# Defining playSound function (called at WASD key-bindings)
def playSounds(self):
		if self.game.levelGen.showBlock() == "Grass":
			grassSound.play()
		elif self.game.levelGen.showBlock() == "Sand":
			sandSound.play()
		elif self.game.levelGen.showBlock() == "Water":
			waterSound.play()

class Player:
	def __init__(self, pos, game):
		self.TEXTURE_FILE = pygame.image.load(path.join(IMG_DIR, 'textures.png')).convert_alpha()
		self.pos = pos
		self.game = game
		self.worldLocation = self.game.getCameraOffset() // 32
		self.playerSpeed = vec(4, 4)
		self.playerMovement = vec(0, 0)
		self.directions = vec(0, 0)
		self.lookingAt = SOUTH
		self.hitbox = (self.worldLocation.x + 20, self.worldLocation.y, 48, 48)

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
					self.game.setGameRunning(False)
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
					# Sound effect
					playSounds(self)
				if event.key == K_a:
					self.directions.x += -1
					# Sound effect
					playSounds(self)
				if event.key == K_s:
					self.directions.y += 1
					# Sound effect
					playSounds(self)
				if event.key == K_d:
					self.directions.x += 1
					# Sound effect
					playSounds(self)
				if event.key == K_SPACE:
					self.game.levelGen.getBlock(self.lookingAt)
				if event.key == K_f:
					# Sound effect
					blockSound.play()
					self.game.levelGen.placeBlock(self.lookingAt)
				if event.key == K_e:
					self.game.levelGen.interactBlock(self.lookingAt)
				if event.key == K_F3:
					self.game.toggleStats()
			