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
AnimationComponent(player, ('media/sprites/fsociety.jpg', 'media/sprites/money.png'), speed=0.05)
ColliderComponent(player)
# AudioComponent(player, 'media/audio/toin.mp3')