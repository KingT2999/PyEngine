import random
from engine.components import *
from engine.camera import Camera
from config import WIDTH, HEIGHT


# Camera
camera = Camera()

# Wall
wall = GameObj()
TransformComponent(wall, 0, 0, WIDTH, HEIGHT)


# PLayer
player = GameObj()
TransformComponent(player, 15, 15, 100, 100)
SpriteComponent(player, 'media/sprites/fsociety.jpg')
ColliderComponent(player)
# AudioComponent(player, 'media/audio/toin.mp3')