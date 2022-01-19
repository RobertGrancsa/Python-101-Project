import pygame

pygame.init()
pygame.display.set_caption('Untitled Game')
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

input()
update()
draw()

class Block:
	def __init__(self, culoare, coordonata):
		self.culoare = culoare
		self.coordonata = coordonata
	
	def draw():
		draw(coordonata, culoare, marime)
		

class Forma(matrice, culoare):
	def __init__(self, culoare, coordonata):
		lista_blocuri = []

		for i in matrice:
			for j in iar_matrice:
				if matrice[i][j]:
					lista_blocuri.append(Block(rosu, i, j))

	def draw():
		for block in lista_blocuri:
			block.draw()



*	*
	*
	*

*	*	*
*

*	*
*	*

