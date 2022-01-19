#! /usr/bin/env python3

import pygame
from game import Game
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

class Camera:
	def __init__(self, game):
		self.game = game
		self.offset = vec(0, 0)
		self.offset_float = vec(0, 0)
		self.CONST = vec(0, 0)

	def setMethod(self, method):
		self.method = method

	def scroll(self):
		self.method.scroll()

class CamScroll(ABC):
	def __init__(self, camera, game) -> None:
		self.camera = camera
		self.game = game

	@abstractmethod
	def scroll(self):
		pass

class Follow(CamScroll):
	def __init__(self, camera, game) -> None:
		CamScroll.__init__(self, camera, game)

	def scroll(self):
		self.camera.offset_float.x += (self.game.playerPawn.pos.x - self.camera.offset_float.x + self.camera.CONST.x)
		self.camera.offset_float.y += (self.game.playerPawn.pos.y - self.camera.offset_float.y + self.camera.CONST.y)
		self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Auto(CamScroll):
	def __init__(self,camera, game) -> None:
		CamScroll.__init__(self,camera, game)

	def scroll(self):
		self.camera.offset.x += 32