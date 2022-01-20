#! /usr/bin/env python3

import threading


import pygame
import noise
import matplotlib.pyplot as plt
import numpy as np
import random as rand
from pygame.image import tostring
from pygame.locals import *
from os import mkdir, path
from constants import *
vec = pygame.math.Vector2
import pickle
import json
from copy import deepcopy

IMG_DIR = path.join(path.dirname(__file__), 'textures')
DATA_DIR = path.join(path.dirname(__file__), 'worldData')

if not path.exists(DATA_DIR):
	mkdir(DATA_DIR)

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

class Interactable(Block):
	def __init__(self, position, texture, canvas, game, type):
		super().__init__(position, texture, canvas, game, type)
		self.rect = pygame.Rect(self.position.x * SIZE, self.position.y * SIZE, SIZE, SIZE)

	def getRect(self):
		return self.rect

	def draw(self):
		self.canvas.blit(self.texture, self.rect)

class Chunk:
	def __init__(self, chunkValues, textureDict, position, game):
		self.chunkValues = chunkValues
		self.textureDict = textureDict
		self.position = position
		self.game = game
		self.alreadyLoaded = False
		self.blockList = []
		self.blockDict = {}

		self.checkAlreadyLoaded()
		self.makeCanvas()

	def getLocation(self):
		return self.position

	def getDict(self):
		return self.blockDict

	def checkAlreadyLoaded(self):
		with open('worldData/chunk.json', "r") as jsonFile:
			data = json.load(jsonFile)

		chunk = data.get(str(str(self.position.x) + ", " + str(self.position.y)))

		if bool(chunk):
			self.alreadyLoaded = True
			self.blockDict = chunk

	def getBlock(self, blockLocation):
		for block in self.blockList:
			if block.getPosition() == blockLocation:
				return block

	def getAnim(self, position):
		frames = []
		for x in range(2):
			frames.append(self.textureDict.subsurface(x * SIZE, 2 * SIZE, SIZE, SIZE))
		return frames

	def addBlock(self, position, entityName):
		block = {}
		block.update({"Type":entityName})
		block.update({"Position":(position.x, position.y)})
		block.update({"Entity":Block(position, self.textureDict.get(str(entityName)), self.canvas, self.game, entityName)})
		self.blockDict.update({str(position):block})

	def addInteractable(self, position, entityName):
		block = {}
		block.update({"Type":entityName})
		block.update({"Position":(position.x, position.y)})
		block.update({"Entity":Interactable(position, self.textureDict.get(str(entityName)), self.canvas, self.game, entityName)})
		self.blockDict.update({str(position):block})

	def makeCanvas(self):
		self.canvas = pygame.Surface((CHUNK_SIZE[0] * SIZE,CHUNK_SIZE[1] * SIZE))

		for i in range(CHUNK_SIZE[0]):
			for j in range(CHUNK_SIZE[1]):
				blockChance = rand.random()
				if self.chunkValues[i][j] < -0.05:
					self.blockList.append(Block(vec(i, j), self.textureDict.get("Water"), self.canvas, self.game, "Water"))
				elif self.chunkValues[i][j] < 0:
					self.blockList.append(Block(vec(i, j), self.textureDict.get("Sand"), self.canvas, self.game, "Sand"))
					if not self.alreadyLoaded:
						if blockChance > 0.95:
							self.addInteractable(vec(i, j), "Palm")
						elif blockChance > 0.9:
							self.addInteractable(vec(i, j), "Cactus")
				elif self.chunkValues[i][j] < 1.0:
					self.blockList.append(Block(vec(i, j), self.textureDict.get("Grass"), self.canvas, self.game, "Grass"))
					if not self.alreadyLoaded:
						if blockChance > 0.995:
							self.addInteractable(vec(i, j), "Chest")
						elif blockChance > 0.8:
							self.addInteractable(vec(i, j), "Tree")
		if self.alreadyLoaded:
			self.loadJSON()

	def loadJSON(self):
		for key in self.blockDict:
			block = self.blockDict.get(key)
			posList = block.get("Position")
			position = vec(posList[0], posList[1])
			block.update({"Entity":Block(position, self.textureDict.get(str(block.get("Type"))), self.canvas, self.game, block.get("Type"))})


	def updateJSON(self):
		if bool(self.blockDict):
			newDict = {}
			data = {}

			with open('worldData/chunk.json', "r") as jsonFile:
				data = json.load(jsonFile)

			for key in self.blockDict:
				entry = self.blockDict.get(key).copy()
				entry.pop("Entity")
				newDict.update({key:entry})


			data.update({str(str(self.position.x) + ", " + str(self.position.y)):newDict})

			with open('worldData/chunk.json', 'w') as filehandle:
				json.dump(data, filehandle)

	def makeChunk(self):
		# Draw the background
		for blocks in self.blockList:
			blocks.draw()

		# Draw the entities
		if bool(self.blockDict):
			for key in self.blockDict:
				self.blockDict.get(key).get("Entity").draw()

		# print(self.blockDict)
		# updateJSON_thread = threading.Thread(target=self.updateJSON, name="updateJSON")
		# updateJSON_thread.start()
		self.updateJSON()

		# font = pygame.font.Font('freesansbold.ttf', 32)
		# text = font.render(str(self.position), True, (255, 0, 0))
		# self.canvas.blit(text, (0, 0))
		return self.canvas

	def updateChunk(self):
		for blocks in self.blockList:
			if blocks.__class__.__name__ == "Water":
				blocks.update()

class LevelGen:
	def __init__(self, game):
		self.TEXTURE_FILE = pygame.image.load(path.join(IMG_DIR, 'textures.png')).convert_alpha()
		self.game = game
		self.world = self.loadWorld()
		self.canvas = pygame.Surface((WIDTH,HEIGHT))
		self.chunks = pygame.Surface((CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2, CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2))
		self.entities = pygame.Surface((CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2, CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2)).convert_alpha()
		self.textureDict = {}

		if not path.exists('worldData/chunk.json'):
			with open('worldData/chunk.json', "w") as jsonFile:
				json.dump(self.textureDict, jsonFile)

		self.addToDict()
		# plt.imshow(self.world, cmap='gray')
		# plt.show()
		# self.entities.blit(self.textureDict.get("Diamond"), (0, 0, 32, 32))
		self.entities.fill((0, 0, 0, 0))

		self.lastLocation = vec(0, 0)
		self.difference = vec(0, 0)
		self.location = vec(0, 0)
		self.chunkList = []
		self.blockList = []
		self.createWorldMap()

		self.lastChunk = self.getChunkLocation(self.game.getCameraOffset())

	def loadWorld(self):
		rand.seed(path.dirname(__file__))
		seed = int(rand.random() * 100)
		print("Seed: " + str(seed) + " " + path.dirname(__file__))

		shape = NOISE_MAP
		scale = 100.0
		octaves = 6
		persistence = 0.5
		lacunarity = 2.0

		self.world = np.zeros(shape)

		if path.exists("worldData/world.data"):
			with open('worldData/world.data', 'rb') as filehandle:
				self.world = pickle.load(filehandle)
		else:
			for i in range(shape[0]):
				for j in range(shape[1]):
					self.world[i][j] = noise.pnoise2(i/scale,
													j/scale,
													octaves=octaves,
													persistence=persistence,
													lacunarity=lacunarity,
													repeatx=NOISE_MAP[0],
													repeaty=NOISE_MAP[1],
													base=seed)
			with open('worldData/world.data', 'wb') as filehandle:
				pickle.dump(self.world, filehandle)

		return self.world

	def addToDict(self):
		self.textureDict.update({"Dirt":self.getTexture(DIRT)})
		self.textureDict.update({"Water":self.getTexture(WATER)})
		self.textureDict.update({"Grass":self.getTexture(GRASS)})
		self.textureDict.update({"Sand":self.getTexture(SAND)})
		self.textureDict.update({"Tree":self.getTexture(TREE)})
		self.textureDict.update({"Wood":self.getTexture(WOOD)})
		self.textureDict.update({"Chest":self.getTexture(CHEST)})
		self.textureDict.update({"Palm":self.getTexture(PALM)})
		self.textureDict.update({"Cactus":self.getTexture(CACTUS)})
		self.textureDict.update({"Diamond":self.getTexture(DIAMOND)})
		self.textureDict.update({"Ruby":self.getTexture(RUBY)})

	# All the getters of this class

	def getTexture(self, position):
		return self.TEXTURE_FILE.subsurface(position[0] * SIZE, position[1] * SIZE, SIZE, SIZE)

	# The position within a chunk
	def getRelativeLocation(self, position):
		relativeLocation = vec(0, 0)
		relativeLocation.x = self.location.x % CHUNK_SIZE[0]
		relativeLocation.y = self.location.y % CHUNK_SIZE[1]
		return relativeLocation

	# The chunk position at the position the player is at
	def getChunkLocation(self, worldLocation):
		chunkPosition = vec(0, 0)
		chunkPosition.x = worldLocation.x // SIZE // CHUNK_SIZE[0]
		chunkPosition.y = worldLocation.y // SIZE // CHUNK_SIZE[1]

		return chunkPosition

	# The chunk the player is in
	def getChunk(self, location):
		chunkOfBlock = self.getChunkLocation(location)
		chunk = 0
		for chunks in self.chunkList:
			for chunk in chunks:
				if chunk.getLocation() == chunkOfBlock:
					currentChunk = chunk
		return currentChunk

	def getBlock(self):
		relativeLocation = vec(0, 0)
		relativeLocation.x = self.location.x % CHUNK_SIZE[0]
		relativeLocation.y = self.location.y % CHUNK_SIZE[1]

		currentChunk = self.getChunk(self.location * SIZE)

		currentBlock = currentChunk.getBlock(relativeLocation)

		return currentBlock

	def getBackground(self):
		return self.chunks

	# ----------------------------- Worldgen stuff ------------------------------

	def createWorldMap(self):
		noiseMapHalf = NOISE_MAP[0] // 2
		currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		self.chunkList.clear()
		for i in range(VIEW_DISTANCE * 2):
			rows = []
			for j in range(VIEW_DISTANCE * 2):
				rows.append(Chunk(self.world[(noiseMapHalf + ((i-VIEW_DISTANCE + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i-VIEW_DISTANCE+1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										(noiseMapHalf + ((j-VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-VIEW_DISTANCE+1 + int(currentChunk.y)) * CHUNK_SIZE[0]))],
										self.textureDict, vec(i-VIEW_DISTANCE + int(currentChunk.x), j-VIEW_DISTANCE + int(currentChunk.y)), self.game))

			self.chunkList.append(rows[:])
			rows.clear()

		self.updateChunk()

	def updateWorldMap(self, diff):		# Problems se misca in intr-un chunk care nu e vecin cu chunk-ul trecut
		currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		noiseMapHalf = NOISE_MAP[0] // 2
		newChunkList = []

		# ---------------------- Change y ---------------
		i = -VIEW_DISTANCE
		if diff.y == -1:
			for rows in self.chunkList:
				newRows = []
				newRows.append(Chunk(self.world[(noiseMapHalf + ((i + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i + 1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
										   		(noiseMapHalf + ((-VIEW_DISTANCE+ int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((-VIEW_DISTANCE + 1 + int(currentChunk.y)) * CHUNK_SIZE[0]))],
										   		self.textureDict, vec(i + int(currentChunk.x), -VIEW_DISTANCE + int(currentChunk.y)), self.game))
				newRows.extend(rows[0:-1])
				newChunkList.append(newRows)

				i += 1
		i = -VIEW_DISTANCE
		if diff.y == 1:
			for rows in self.chunkList:
				newRows = []
				newRows.extend(rows[1:])
				newRows.append(Chunk(self.world[(noiseMapHalf + ((i + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((i + 1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
												(noiseMapHalf + ((VIEW_DISTANCE - 1 + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0]))],
												self.textureDict, vec(i + int(currentChunk.x), VIEW_DISTANCE - 1 + int(currentChunk.y)), self.game))
				newChunkList.append(newRows)

				i += 1

		# ---------------------- Change x ---------------
		if diff.x == -1:
			newRows = []
			for j in range(VIEW_DISTANCE * 2):
				newRows.append(Chunk(self.world[(noiseMapHalf + ((-VIEW_DISTANCE + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((-VIEW_DISTANCE + 1 + int(currentChunk.x)) * CHUNK_SIZE[0])),
												(noiseMapHalf + ((j-VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-VIEW_DISTANCE+1 + int(currentChunk.y)) * CHUNK_SIZE[0]))],
												self.textureDict, vec(-VIEW_DISTANCE + int(currentChunk.x), j - VIEW_DISTANCE + int(currentChunk.y)), self.game))
			newChunkList.append(newRows)
			newChunkList.extend(self.chunkList[0:-1])

		if diff.x == 1:
			newRows = []
			newChunkList.extend(self.chunkList[1:])
			for j in range(VIEW_DISTANCE * 2):
				newRows.append(Chunk(self.world[(noiseMapHalf + ((VIEW_DISTANCE - 1 + int(currentChunk.x)) * CHUNK_SIZE[0])):(noiseMapHalf + ((VIEW_DISTANCE + int(currentChunk.x)) * CHUNK_SIZE[0])),
												(noiseMapHalf + ((j-VIEW_DISTANCE + int(currentChunk.y)) * CHUNK_SIZE[0])):(noiseMapHalf + ((j-VIEW_DISTANCE+1 + int(currentChunk.y)) * CHUNK_SIZE[0]))],
												self.textureDict, vec(VIEW_DISTANCE - 1 + int(currentChunk.x), j - VIEW_DISTANCE + int(currentChunk.y)), self.game))
			newChunkList.append(newRows)
		self.chunkList = newChunkList[:]
		self.updateChunk()
		# self.cropEntityLayer()

	# def multipleChunkLoad(self, difference):
	# 	if abs(difference.x) == 2:
	# 		difference.x /= difference.x
	# 		self.updateWorldMap(difference)
	# 	elif abs(difference.y) == 2:
	# 		difference.y /= difference.y
	# 		self.updateWorldMap(difference)
	# 	else:
	# 		self.updateWorldMap(difference)
	# 	self.updateWorldMap(difference)
	# 	self.updateChunk()

	def showPos(self):
		self.location = self.game.getCameraOffset() // SIZE
		self.chunk = self.getChunkLocation(self.location * SIZE)
		return (self.location, self.chunk)

	def showBlock(self):
		return self.getBlock().getType()

	def interactBlock(self, direction):
		relativeLocation = self.getRelativeLocation(self.game.getCameraOffset())
		chunk = self.getChunk(self.location)
		name = ''

		# relativeLocation += direction

		dictionary = chunk.getDict()
		# print(dictionary)
		block = dictionary.get(str(relativeLocation))
		if bool(block):
			name = block.get("Type")
		
		if name == "Chest":
			number = rand.randrange(5, 15)
			
			self.game.incrementTimer(number)
			print("Incremented")
		# self.addToWorld(chunk.getLocation(), relativeLocation)

	def placeBlock(self, direction):
		relativeLocation = self.getRelativeLocation(self.game.getCameraOffset())
		chunk = self.getChunk(self.location * SIZE)

		relativeLocation += direction

		chunk.addBlock(relativeLocation, "Wood")
		chunk.makeChunk()
		self.updateChunk()
		print("Placed block at " + str(relativeLocation))

	def addToWorld(self, chunkPos, relativePos):
		drop = self.textureDict.get("Ruby")
		print("Added diamond at " + str(chunkPos) + str(relativePos))
		print(self.difference)

		self.entities.blit(drop, (((VIEW_DISTANCE) * CHUNK_SIZE[0] + relativePos.x) * SIZE, ((VIEW_DISTANCE) * CHUNK_SIZE[1] + relativePos.y) * SIZE))

	def cropEntityLayer(self):
		print(self.difference)
		self.difference.x = int(self.difference.x)
		self.difference.y = int(self.difference.y)

		chunkOffset = vec(self.currentChunk.x * SIZE * CHUNK_SIZE[0], self.currentChunk.y * SIZE * CHUNK_SIZE[1])

		print('Sizes: {} {} {} {}'.format(chunkOffset.x, chunkOffset.y, CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2 + chunkOffset.x,
											CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2 - chunkOffset.y))
		
		cropped = self.entities.subsurface(max(chunkOffset.x, 0), max(chunkOffset.y, 0), CHUNK_SIZE[0] * SIZE * VIEW_DISTANCE * 2 + chunkOffset.x,
											CHUNK_SIZE[1] * SIZE * VIEW_DISTANCE * 2 - chunkOffset.y)

		# self.entities.fill((0, 0, 0, 0))
		# self.entities.blit(cropped, (-chunkOffset.x, -chunkOffset.y))

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
			self.difference = currentChunk - self.lastChunk
			print("Difference: " + str(self.difference))

			self.lastLocation = self.lastChunk
			loadChunks_thread = threading.Thread(target=self.updateWorldMap, name="Chunks", args=(self.difference,))
			loadChunks_thread.start()

			print("Updated chunks" + str(self.getChunkLocation(self.game.getCameraOffset())))

		self.lastChunk = self.getChunkLocation(self.game.getCameraOffset())

	def update(self):
		# self.location = self.game.getCameraOffset()
		self.currentChunk = self.getChunkLocation(self.game.getCameraOffset())
		offset = self.game.getCameraOffset()

		self.changedChunk()

		# Very important - the 0, 0 coordinates are counted from here
		self.origin = vec(SIZE * CHUNK_SIZE[0] * (self.lastLocation.x) + (-1 * (SIZE * CHUNK_SIZE[0] * VIEW_DISTANCE // 2)) - offset.x - 260,
					 	  SIZE * CHUNK_SIZE[0] * (self.lastLocation.y - 1) + (-1 * (SIZE * CHUNK_SIZE[0] * VIEW_DISTANCE // 2))  - offset.y + 144)

		self.game.screen.blit(self.chunks, (self.origin.x, self.origin.y))
		self.game.screen.blit(self.entities, (self.origin.x, self.origin.y))

	def collision(self):
		relativeLocation = vec(0, 0)
		relativeLocation.x = self.location.x % CHUNK_SIZE[0]
		relativeLocation.y = self.location.y % CHUNK_SIZE[1]

		chunk = self.getChunk(self.location * SIZE)
		dict = chunk.getDict()
		
		# block = dict.get(str(str(self.relativeLocation.x) + ", " + str(self.relativeLocation.y)))
		# if bool(block):
			# print("im on smth")


