#! /usr/bin/env python3

import pygame
vec = pygame.math.Vector2

SIZE = 32
BLOCK = (32, 32)

WIDTH = 1920
HEIGHT = 1080
FPS = 60

# Player vision
VIEW_DISTANCE = 4
CHUNK_SIZE = (16, 16)

# Texture location
DIRT = (0, 0)
GRASS = (1, 0)
WATER = (2, 0)
WATER_ANIM = ((0, 2), (2, 2))
SAND = (3, 0)
WOOD = (4, 0)
NOTHING = (0, 1)
TREE = (1, 1)

PLAYER_FRONT = (2, 1)
PLAYER_BACK = (3, 1)
PLAYER_LEFT = (4, 1)
PLAYER_RIGHT = (5, 1)

NORTH = vec(0, 1)
EAST  = vec(1, 0)
SOUTH = vec(0,-1)
WEST  = vec(-1,0)
