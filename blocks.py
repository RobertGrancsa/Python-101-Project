#! /usr/bin/env python3

import pygame
import noise
import numpy as np
from pygame.locals import *
from os import path
from constants import *
vec = pygame.math.Vector2

IMG_DIR = path.join(path.dirname(__file__), 'textures')

shape = (1024, 1024)
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=0)

class Block:
	def __init__(self, position, texture, canvas):
		self.position = position
		self.texture = texture
		self.canvas = canvas

	def getPosition(self):
		return self.position

	def draw(self):
		self.canvas.blit(self.texture, (self.position.x * SIZE, self.position.y * SIZE))

class Chunk:
	def __init__(self, chunkValues, worldTexture, position):
		self.chunkValues = chunkValues
		self.worldTexture = worldTexture
		self.position = position

		self.blockList = []
		self.makeCanvas()
		
	def getTexture(self, position):
		return self.worldTexture.subsurface(position[0] * SIZE, position[1] * SIZE, SIZE, SIZE)

	def makeCanvas(self):
		self.canvas = pygame.Surface((CHUNK_SIZE[0] * SIZE,CHUNK_SIZE[1] * SIZE))

		for i in range(CHUNK_SIZE[0]):
			for j in range(CHUNK_SIZE[1]):
				if self.chunkValues[i][j] < -0.05:
					self.blockList.append(Block(vec(i, j), self.getTexture(WATER), self.canvas))
				elif self.chunkValues[i][j] < 0:
					self.blockList.append(Block(vec(i, j), self.getTexture(SAND), self.canvas))
				elif self.chunkValues[i][j] < 1.0:
					self.blockList.append(Block(vec(i, j), self.getTexture(GRASS), self.canvas))

	def makeChunk(self):
		for blocks in self.blockList:
			blocks.draw()

		font = pygame.font.Font('freesansbold.ttf', 32)
		text = font.render(str(self.position), True, (255, 0, 0))
		self.canvas.blit(text, (0, 0))
		return self.canvas

class LevelGen:
	def __init__(self, game):
		self.TEXTURE_FILE = pygame.image.load(path.join(IMG_DIR, 'textures.png')).convert()
		self.game = game
		self.canvas = pygame.Surface((WIDTH,HEIGHT))
		self.chunks = pygame.Surface((CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2, CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2))

		self.chunkList = []
		self.blockList = []
		self.createWorldMap()
		self.updateChunk()

		self.lastChunk = self.getChunk(self.game.getCameraOffset())

	def createWorldMap(self):
		noiseMapHalf = 1024 // 2
		currentChunk = self.getChunk(self.game.getCameraOffset())
		self.chunkList.clear()
		for i in range(VIEW_DISTANCE * 2):
			rows = []
			for j in range(VIEW_DISTANCE * 2):
				rows.append(Chunk(world[(noiseMapHalf + ((i-4 + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i-3 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										(noiseMapHalf + ((j-4 + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-3 + int(currentChunk.y)) * CHUNK_SIZE[0]))], 
										self.TEXTURE_FILE, vec(i-4 + int(currentChunk.x), j-4 + int(currentChunk.y))))
			
			self.chunkList.append(rows[:])
			rows.clear()

	def getChunk(self, worldLocation):
		chunkPosition = vec(0, 0)
		chunkPosition.x = worldLocation.x // SIZE // CHUNK_SIZE[0]
		chunkPosition.y = worldLocation.y // SIZE // CHUNK_SIZE[1]

		return chunkPosition

	def updateChunk(self):
		for i in range(VIEW_DISTANCE * 2):
			for j in range(VIEW_DISTANCE * 2):
				self.chunks.blit(self.chunkList[i][j].makeChunk(), ((i) * CHUNK_SIZE[0] * SIZE, (j) * CHUNK_SIZE[1] * SIZE))

	def changedChunk(self):
		if self.getChunk(self.game.getCameraOffset()) != self.lastChunk:
			self.createWorldMap()
			self.updateChunk()
			print("Updated chunks" + str(self.getChunk(self.game.getCameraOffset())))
		
		self.lastChunk = self.getChunk(self.game.getCameraOffset())


	def update(self):
		currentChunk = self.getChunk(self.game.getCameraOffset())
		offset = self.game.getCameraOffset()

		self.changedChunk()
		
		self.game.screen.blit(self.chunks, (SIZE * CHUNK_SIZE[0] *currentChunk.x + (-1 * (SIZE * CHUNK_SIZE[0] * VIEW_DISTANCE // 2)) - offset.x,
											SIZE * CHUNK_SIZE[0] *currentChunk.y + (-1 * (SIZE * CHUNK_SIZE[0] * VIEW_DISTANCE // 2))  - offset.y))
	
