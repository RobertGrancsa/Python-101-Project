#! /usr/bin/env python3

import pygame
vec = pygame.math.Vector2

GAME_NAME = 'Epic Game'

# Menu
BUTTON_SIZE = (256, 82)
B_W = 512
B_H = 164


# Worldgen
SIZE = 32
BLOCK = (32, 32)
NOISE_MAP = (1024, 1024)


WIDTH = 512
HEIGHT = 288
FPS = 60

# Player vision
VIEW_DISTANCE = 2
CHUNK_SIZE = (16, 16)

# Texture location
DIRT = (0, 0)
GRASS = (1, 0)
WATER = (2, 0)
WATER_ANIM = ((0, 2), (2, 2))
SAND = (3, 0)
WOOD = (4, 0)
CHEST = (0, 2)
CACTUS = (1, 2)
TREE = (2, 2)
PALM = (3, 2)

DIAMOND = (0, 3)
RUBY = (1, 3)
EMERALD = (2, 3)
NOTHING = (0, 1)

PLAYER_FRONT = (2, 1)
PLAYER_BACK = (3, 1)
PLAYER_LEFT = (4, 1)
PLAYER_RIGHT = (5, 1)

NORTH = vec(0, -1)
EAST  = vec(1, 0)
SOUTH = vec(0,1)
WEST  = vec(-1,0)

# Inventory
INVENTORY_SIZE = INVENTORY_WIDTH, INVENTORY_HEIGHT = (
    600,
    600,
)

INVENTORY_COORDS = INVENTORY_X, INVENTORY_Y = (
    WIDTH // 2 - INVENTORY_WIDTH // 2,
    HEIGHT // 2 - INVENTORY_HEIGHT // 2,
)

SELECTION_BOX_THICKNESS = 20
