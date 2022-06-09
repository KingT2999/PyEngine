from engine.components import *
from engine.camera import Camera
from config import WIDTH, HEIGHT


# Camera
camera = Camera()

# Wall
wall = GameObj()
TransformComponent(wall, 0, 0, WIDTH, HEIGHT)


# PLayer
hacker = GameObj()
TransformComponent(hacker, 15, 15, 100, 100)
SpriteComponent(hacker, 'media/sprites/fsociety.jpg')
ColliderComponent(hacker)
# AudioComponent(hacker, 'media/audio/toin.mp3')