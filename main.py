# from box import *
# from uiClass import *
import time
from math import cos, sin, pi
from game import Game
import sys
import pygame
from earth import Earth 
from cloud import Cloud
from player import Player
import random
pygame.font.init()
pygame.init()

img = pygame.image.load('assets/Earth.png')

pygame.display.set_icon(img)
pygame.display.set_caption('HackGwinnet3')

Clock = pygame.time.Clock()
frame_rate = 60

MAPSIZE = 16 #number of slots on the earth
MAP_RADIUS = 64; # px
ATMOS_RADIUS = 128; # px
#objects on map
map = [ 0 for i in range(MAPSIZE) ]
# POSITIONS = [ #map locatons in absolute pixels
#   (MAP_RADIUS * cos(i * 2 * pi), MAP_RADIUS * sin(i * 2 * pi)) for i in range(MAPSIZE)
# ]
angles = 1 / MAPSIZE # in tau

screen = pygame.display.set_mode((960, 540))
pygame.display.set_caption('Hello World!')
BG_COLOR = 'light gray'
block_size = 32

earth = Earth(MAP_RADIUS, ATMOS_RADIUS, 8, "assets/Earth.png")
player = Player( 8, (255,255,0), MAP_RADIUS)
cloud0 = Cloud( ATMOS_RADIUS, screen.get_height() / 2, 0, 10, 10)

game = Game(screen, map, earth, player, cloud0) # create first game

def main(): 
    prevtime = time.time()
    secondCounter = 0
    while True: #the only cycle
        dt = time.time() - prevtime #unit is milisecond/frame
        prevtime = time.time()
        secondCounter += dt

        if (secondCounter >= 1 ):
            game.add_cloud( Cloud( ATMOS_RADIUS, screen.get_height() / 2, random.random(), 10, 10) )
            secondCounter = 0

        game.update(dt)
        game.draw()

enemies = pygame.sprite.Group()  # group of enemy clouds


if __name__ == '__main__':
    main()
# box = Box(
#     screen,
#     lambda x, y: (x//2, y//2),
#     lambda x, y: (x//2, y//5),
#     'white',
#     'green',
#     10,
#     'black',
#     10,
#     Direction.topleft,
#     True,
# )

# image_box = Image(
#     'tree.jpg',
#     pygame.BLEND_RGBA_MIN,
#     10,
#     box.set_pos_func(lambda x, y: (10, 10)),
#     resize_image_to_box = False,
# )

# text_box = TextBox(
#     '1234',
#     'black',
#     20,
#     'arial',
#     True,
#     Direction.center,
#     OverflowingOptions.resize_box_down,
#     True,
#     10,
#     image_box
#