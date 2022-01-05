#! /usr/bin/env python3

import threading
from types import NoneType

import pygame
import noise
import numpy as np
import random as rand
from pygame.image import tostring
from pygame.locals import *
from os import path
from constants import *
vec = pygame.math.Vector2

IMG_DIR = path.join(path.dirname(__file__), 'textures')

rand.seed(0)

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
	def __init__(self, position, texture, canvas, game, type):
		self.position = position
		self.texture = texture
		self.canvas = canvas
		self.game = game
		self.type = type

	def getType(self):
		return self.type

	def getPosition(self):
		return self.position

	def draw(self):
		self.canvas.blit(self.texture, (self.position.x * SIZE, self.position.y * SIZE))

class Tree(Block):
	def __init__(self, position, texture, canvas, game, type):
		super().__init__(position, texture, canvas, game, type)

	def collision(self):
		pass

	def draw(self):
		return super().draw()

class Water(Block):
	def __init__(self, position, texture, canvas, game, type):
		super().__init__(position, texture, canvas, game, type)
		self.currentTime = 0
		self.animationTime = 1/3
		self.index = 0

	def collision(self):
		pass

	def draw(self):
		self.canvas.blit(self.texture, (self.position.x * SIZE, self.position.y * SIZE))

	def changeTexture(self, deltaT):
		self.currentTime += deltaT
		if self.currentTime >= self.animationTime:
			self.currentTime = 0
			self.index = (self.index + 1) % len(self.texture)
		return self.texture[self.index]

	def update(self, deltaT):
		self.currentTexture = self.changeTexture()
		self.canvas.blit(self.currentTexture, (self.position.x * SIZE, self.position.y * SIZE))

class Chunk:
	def __init__(self, chunkValues, worldTexture, position, game):
		self.chunkValues = chunkValues
		self.worldTexture = worldTexture
		self.position = position
		self.game = game

		self.blockList = []
		self.makeCanvas()

	def getLocation(self):
		return self.position

	def getBlock(self, blockLocation):
		for block in self.blockList:
			if block.getPosition() == blockLocation:
				print(block)
				return block
		
	def getTexture(self, position):
		return self.worldTexture.subsurface(position[0] * SIZE, position[1] * SIZE, SIZE, SIZE)

	def getAnim(self, position):
		frames = []
		for x in range(2):
			frames.append(self.worldTexture.subsurface(x * SIZE, 2 * SIZE, SIZE, SIZE))
		return frames

	def addBlock(self, position, type):
		self.blockList.append(Block(position, self.getTexture(type[0]), self.canvas, self.game, type[1]))
		

	def makeCanvas(self):
		self.canvas = pygame.Surface((CHUNK_SIZE[0] * SIZE,CHUNK_SIZE[1] * SIZE))

		for i in range(CHUNK_SIZE[0]):
			for j in range(CHUNK_SIZE[1]):
				if self.chunkValues[i][j] < -0.05:
					self.blockList.append(Water(vec(i, j), self.getTexture(WATER), self.canvas, self.game, "Water"))
				elif self.chunkValues[i][j] < 0:
					self.blockList.append(Block(vec(i, j), self.getTexture(SAND), self.canvas, self.game, "Sand"))
				elif self.chunkValues[i][j] < 1.0:
					self.blockList.append(Block(vec(i, j), self.getTexture(GRASS), self.canvas, self.game, "Grass"))
					treeChance = rand.random()
					if treeChance > 0.8:
						self.blockList.append(Tree(vec(i, j), self.getTexture(TREE), self.canvas, self.game, "Tree"))

	def makeChunk(self):
		for blocks in self.blockList:
			blocks.draw()

		font = pygame.font.Font('freesansbold.ttf', 32)
		text = font.render(str(self.position), True, (255, 0, 0))
		self.canvas.blit(text, (0, 0))
		return self.canvas

	def updateChunk(self):
		for blocks in self.blockList:
			if blocks.__class__.__name__ == "Water":
				blocks.update()

class LevelGen:
	def __init__(self, game):
		self.TEXTURE_FILE = pygame.image.load(path.join(IMG_DIR, 'textures.png')).convert_alpha()
		self.game = game
		self.canvas = pygame.Surface((WIDTH,HEIGHT))
		self.chunks = pygame.Surface((CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2, CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2))

		self.lastLocation = vec(0, 0)
		self.chunkList = []
		self.blockList = []
		self.createWorldMap()

		self.lastChunk = self.getChunkLocation(self.game.getCameraOffset())

	def createWorldMap(self):
		noiseMapHalf = 1024 // 2
		currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		self.chunkList.clear()
		for i in range(VIEW_DISTANCE * 2):
			rows = []
			for j in range(VIEW_DISTANCE * 2):
				rows.append(Chunk(world[(noiseMapHalf + ((i-VIEW_DISTANCE + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i-VIEW_DISTANCE+1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										(noiseMapHalf + ((j-VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-VIEW_DISTANCE+1 + int(currentChunk.y)) * CHUNK_SIZE[0]))], 
										self.TEXTURE_FILE, vec(i-4 + int(currentChunk.x), j-4 + int(currentChunk.y)), self.game))
			
			self.chunkList.append(rows[:])
			rows.clear()
		
		self.updateChunk()
	def updateWorldMap(self, diff):		# Problems se misca in intr-un chunk care nu e vecin cu chunk-ul trecut
		currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		noiseMapHalf = 1024 // 2
		newChunkList = []

		# ---------------------- Change y ---------------
		i = -4
		if diff.y == -1:
			for rows in self.chunkList:
				newRows = []
				newRows.append(Chunk(world[(noiseMapHalf + ((i + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i + 1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										   (noiseMapHalf + ((-VIEW_DISTANCE+ int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((-VIEW_DISTANCE + 1 + int(currentChunk.y)) * CHUNK_SIZE[0]))], 
										   self.TEXTURE_FILE, vec(i + int(currentChunk.x), -VIEW_DISTANCE + int(currentChunk.y)), self.game))
				newRows.extend(rows[0:-1])
				newChunkList.append(newRows)

				i += 1
		i = -4
		if diff.y == 1:
			for rows in self.chunkList:
				newRows = []
				newRows.extend(rows[1:])
				newRows.append(Chunk(world[(noiseMapHalf + ((i + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i + 1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										   (noiseMapHalf + ((VIEW_DISTANCE - 1 + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0]))], 
										   self.TEXTURE_FILE, vec(i + int(currentChunk.x), VIEW_DISTANCE - 1 + int(currentChunk.y)), self.game))
				newChunkList.append(newRows)

				i += 1

		# ---------------------- Change x ---------------
		if diff.x == -1:
			newRows = []
			for j in range(VIEW_DISTANCE * 2):
				newRows.append(Chunk(world[(noiseMapHalf + ((-VIEW_DISTANCE + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((-VIEW_DISTANCE + 1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										   (noiseMapHalf + ((j-VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-VIEW_DISTANCE+1 + int(currentChunk.y)) * CHUNK_SIZE[0]))], 
										   self.TEXTURE_FILE, vec(-VIEW_DISTANCE + int(currentChunk.x), j - VIEW_DISTANCE + int(currentChunk.y)), self.game))
			newChunkList.append(newRows)
			newChunkList.extend(self.chunkList[0:-1])
				
		i = -4
		if diff.x == 1:
			newRows = []
			newChunkList.extend(self.chunkList[1:])
			for j in range(VIEW_DISTANCE * 2):
				newRows.append(Chunk(world[(noiseMapHalf + ((VIEW_DISTANCE - 1 + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((VIEW_DISTANCE + int(currentChunk.x)) * CHUNK_SIZE[0])),
										   (noiseMapHalf + ((j-VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-VIEW_DISTANCE+1 + int(currentChunk.y)) * CHUNK_SIZE[0]))], 
										   self.TEXTURE_FILE, vec(VIEW_DISTANCE - 1 + int(currentChunk.x), j - VIEW_DISTANCE + int(currentChunk.y)), self.game))
			newChunkList.append(newRows)
		self.chunkList = newChunkList[:]
		self.updateChunk()

	def getChunkLocation(self, worldLocation):
		chunkPosition = vec(0, 0)
		chunkPosition.x = worldLocation.x // SIZE // CHUNK_SIZE[0]
		chunkPosition.y = worldLocation.y // SIZE // CHUNK_SIZE[1]

		return chunkPosition

	def showPos(self):
		location = self.game.getCameraOffset() // SIZE
		chunk = self.getChunkLocation(location * SIZE)
		return (location, chunk)

	def showBlock(self):
		return self.getBlock().getType()

	def getBlock(self):
		location = self.game.getCameraOffset() // SIZE
		relativeLocation = vec(0, 0)
		relativeLocation.x = location.x % 16
		relativeLocation.y = location.y % 16
		
		currentChunk = self.getChunk(location * SIZE)

		print(relativeLocation)
		currentBlock = currentChunk.getBlock(relativeLocation)
		print(currentChunk)

		print("Looking at " + currentBlock.getType())

		return currentBlock

	def getChunk(self, location):
		chunkOfBlock = self.getChunkLocation(location)
		for chunks in self.chunkList:
			for chunk in chunks:
				if chunk.getLocation() == chunkOfBlock:
					currentChunk = chunk
		return currentChunk

	def placeBlock(self, direction):
		location = self.game.getCameraOffset() // SIZE
		relativeLocation = vec(0, 0)
		relativeLocation.x = location.x % 16
		relativeLocation.y = location.y % 16
		chunk = self.getChunk(location * SIZE)

		relativeLocation += direction

		chunk.addBlock(relativeLocation, (WOOD, "Wood"))
		chunk.makeChunk()
		self.updateChunk()
		print("Placed block at " + str(relativeLocation))

	def updateChunk(self):
		chunksTmp = pygame.Surface((CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2, CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2))
		for i in range(VIEW_DISTANCE * 2):
			for j in range(VIEW_DISTANCE * 2):
				chunksTmp.blit(self.chunkList[i][j].makeChunk(), (i * CHUNK_SIZE[0] * SIZE, j * CHUNK_SIZE[1] * SIZE))
		self.chunks = chunksTmp
		self.lastLocation = self.getChunkLocation(self.game.getCameraOffset())

	def changedChunk(self):
		currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		
		if currentChunk != self.lastChunk:
			self.lastLocation = self.lastChunk
			difference = currentChunk - self.lastChunk
			
			loadChunks_thread = threading.Thread(target=self.updateWorldMap, name="Chunks", args=(difference,))
			loadChunks_thread.start()
	
			print("Updated chunks" + str(self.getChunkLocation(self.game.getCameraOffset())))

		self.lastChunk = self.getChunkLocation(self.game.getCameraOffset())


	def update(self):
		currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		offset = self.game.getCameraOffset()

		self.changedChunk()

		# Very important - the 0, 0 coordinates are counted from here
		self.origin = vec(SIZE * CHUNK_SIZE[0] * (self.lastLocation.x) + (-1 * (SIZE * CHUNK_SIZE[0] * VIEW_DISTANCE // 2)) - offset.x - 64,
					 SIZE * CHUNK_SIZE[0] * (self.lastLocation.y - 1) + (-1 * (SIZE * CHUNK_SIZE[0] * VIEW_DISTANCE // 2))  - offset.y + 32)

		self.game.screen.blit(self.chunks, (self.origin.x, self.origin.y))
	
