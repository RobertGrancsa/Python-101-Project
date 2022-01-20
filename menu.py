#! /usr/bin/env python3
import sys
import pygame
from pygame.locals import *
from os import path
from inventory import Inventory
from constants import *
from os import mkdir, path

IMG_DIR = path.join(path.dirname(__file__), 'textures')
DATA_DIR = path.join(path.dirname(__file__), 'worldData')

# Initializing mouse-click sound effect (used at line 49)
from pygame import mixer
clickSound = mixer.Sound('audio/click.wav')

class Menu:
	def __init__(self, game):
		self.game = game
		self.click = False
		self.anim = 0
		self.multipliers = 1
		self.pos = 0
		self.up = True
		self.font = pygame.font.Font('font.ttf', 48)
		self.canvas = pygame.Surface((1920, 1080))

		self.textures = pygame.image.load(path.join(IMG_DIR, 'buttons.png'))
		self.background = self.game.levelGen.getBackground()

		self.button = pygame.transform.scale(self.textures.subsurface(0, BUTTON_SIZE[1] * 0, BUTTON_SIZE[0], BUTTON_SIZE[1]), (B_W, B_H))
		self.button_hover = pygame.transform.scale(self.textures.subsurface(0, BUTTON_SIZE[1] * 1, BUTTON_SIZE[0], BUTTON_SIZE[1]), (B_W, B_H))
		self.button_pressed = pygame.transform.scale(self.textures.subsurface(0, BUTTON_SIZE[1] * 2, BUTTON_SIZE[0], BUTTON_SIZE[1]), (B_W, B_H))

		self.make_background(0)
	def make_background(self, perc):
		self.pos += perc * 32
		background = self.game.levelGen.getBackground()
		mirror = pygame.transform.flip(background, True, False)
		if self.pos > mirror.get_width():
			tmp = mirror
			mirror = background
			background = tmp
			self.pos = 0
		self.canvas.blit(mirror, (mirror.get_width() - self.pos, 0, 1920, 1080))
		self.canvas.blit(background, (-self.pos, 0, 1920, 1080))

	def make_button(self):
		button_1 = pygame.Rect(1920 // 2 - B_W // 2 , 400, B_W, B_H)
		button_2 = pygame.Rect(1920 // 2 - B_W // 2 , 600, B_W, B_H)

		mx, my = pygame.mouse.get_pos()
		if button_1.collidepoint((mx, my)):
			self.canvas.blit(self.button_hover, button_1)
			if self.click:
				self.canvas.blit(self.button_pressed, button_1)
				# Sound effect
				clickSound.play()
				self.game.setMenuDisplay(False)
		else:
			self.canvas.blit(self.button, button_1)

		if button_2.collidepoint((mx, my)):
			self.canvas.blit(self.button_hover, button_2)
			if self.click:
				self.canvas.blit(self.button_pressed, button_2)
				self.game.setGameRunning(False)
				self.game.setMenuDisplay(False)
		else:
			self.canvas.blit(self.button, button_2)

		text1 = self.font.render("START GAME", False, (0, 0, 0))
		self.canvas.blit(text1, (1920 // 2 - text1.get_width() // 2, 400 + B_H // 2 - text1.get_height() // 2))
		text1 = self.font.render("START GAME", False, (255, 255, 255))
		self.canvas.blit(text1, (1920 // 2 - text1.get_width() // 2 - 3, 400 + B_H // 2 - text1.get_height() // 2 - 3))
		text2 = self.font.render("END GAME", False, (0, 0, 0))
		self.canvas.blit(text2, (1920 // 2 - text2.get_width() // 2, 600 + B_H // 2 - text2.get_height() // 2))
		text2 = self.font.render("END GAME", False, (255, 255, 255))
		self.canvas.blit(text2, (1920 // 2 - text2.get_width() // 2 - 3, 600 + B_H // 2 - text2.get_height() // 2 - 3))

		self.click = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.game.setGameRunning(False)
					self.game.setMenuDisplay(False)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.click = True

	def animateTitle(self, perc):
		perc /= self.multipliers
		if (self.anim < 1.5) and self.up:
			self.anim += perc
		elif self.anim <= 1:
			self.up = True
		else:
			self.anim -= perc
			self.up = False
			self.multipliers = 2
		
		title = self.font.render(GAME_NAME, False, (255, 255, 255))
		title = pygame.transform.scale(title, (title.get_width() * 2 * self.anim, title.get_height() * 2 * self.anim))
		self.canvas.blit(title, (1920 // 2 - title.get_width() // 2, 100))
		# print(perc)

	def update(self):
		self.game.levelGen.changedChunk()
		self.make_background(self.game.deltaT)
		self.make_button()
		self.animateTitle(self.game.deltaT)
		return self.canvas

	