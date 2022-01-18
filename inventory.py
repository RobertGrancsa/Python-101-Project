import pygame
from pygame.locals import *

from random import randint

import constants as c

class Inventory(object):
	def __init__(self):
		self.active_item = [0, 0]

		self.rect = pygame.Rect(
			c.INVENTORY_X, c.INVENTORY_Y, c.INVENTORY_WIDTH, c.INVENTORY_HEIGHT
		)

		self.sample_item_colors = []

		for i in range(4):
			self.sample_item_colors.append([])
			for j in range(4):
				r, g, b = randint(50, 255), randint(50, 255), randint(50,255)
				self.sample_item_colors[i].append((r, g, b))

	def update(self):
		for event in pygame.event.get():
			if event.type == KEYUP:
				if event.key == K_DOWN:
					self.active_item[1] += 1
				if event.key == K_UP:
					self.active_item[1] += -1
				if event.key == K_LEFT:
					self.active_item[0] -= 1
				if event.key == K_RIGHT:
					self.active_item[0] += 1
			if event.type == KEYDOWN:
				if event.key == K_DOWN:
					self.active_item[1] += 1
					if self.active_item[1] == 4:
						self.active_item[1] = 0
				elif event.key == K_UP:
					self.active_item[1] += -1
					if self.active_item[1] == -1:
						self.active_item[1] = 3
				elif event.key == K_LEFT:
					self.active_item[0] -= 1
					if self.active_item[0] == -1:
						self.active_item[0] = 3
				elif event.key == K_RIGHT:
					self.active_item[0] += 1
					if self.active_item[0] == 4:
						self.active_item[0] = 0

	def draw(self, screen: pygame.Surface):
		pygame.draw.rect(screen, (172, 237, 182), self.rect)

		item_rect = self.rect.copy()
		item_rect.size = 150, 150

		for i in range(4):
			item_rect.x = self.rect.x + (i * 150)
			for j in range(4):
				item_rect.y = self.rect.y + (j * 150)

				pygame.draw.rect(screen, self.sample_item_colors[i][j], item_rect)

		selection_box = self.rect.copy()
		selection_box.size = 150, 150
		selection_box.x += (self.active_item[0] * 150) + (c.SELECTION_BOX_THICKNESS // 2)
		selection_box.y += (self.active_item[1] * 150) + (c.SELECTION_BOX_THICKNESS // 2)
		selection_box.width -= c.SELECTION_BOX_THICKNESS
		selection_box.height -= c.SELECTION_BOX_THICKNESS

		pygame.draw.rect(screen, (255, 255, 255), selection_box, c.SELECTION_BOX_THICKNESS)