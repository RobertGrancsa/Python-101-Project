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
		self.font = pygame.font.Font('freesansbold.ttf', 32)
		self.canvas = pygame.Surface((1920, 1080))
	def make_background(self):
		background = pygame.image.load(path.join(IMG_DIR, 'background.jpg'))
		self.canvas.blit(background, (0, 0, 1920, 1080))
	def make_button(self):
		button1 = pygame.image.load(path.join(IMG_DIR, 'button1.png'))
		button2 = pygame.image.load(path.join(IMG_DIR, 'button1.png'))
		B_WIDTH = 400
		B_HEIGHT = 100

		B_W = 600
		B_H = 400

		button_1 = pygame.Rect(1920 // 2 - B_WIDTH // 2 , 250, B_H, B_W)
		self.canvas.blit(button1, button_1)
		text1 = self.font.render("START GAME", True, (255, 255, 255))
		self.canvas.blit(text1, (1920 // 2 - text1.get_width() // 2, 300))

		button_2 = pygame.Rect(1920 // 2 - B_WIDTH // 2 , 550, B_H, B_W)
		self.canvas.blit(button2, button_2)
		text2 = self.font.render("END GAME", True, (255, 255, 255))
		self.canvas.blit(text2, (1920 // 2 - text2.get_width() // 2, 600))

		mx, my = pygame.mouse.get_pos()
		if button_1.collidepoint((mx, my)):
			if self.click:
				# Sound effect
				clickSound.play()
				self.game.setMenuDisplay(False)
		if button_2.collidepoint((mx, my)):
			if self.click:
				pygame.quit()
				sys.exit()

		self.click = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.click = True

	def update(self):
		self.make_background()
		self.make_button()
		return self.canvas

	