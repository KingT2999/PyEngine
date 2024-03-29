import random
from engine.components import *
from engine.camera import Camera
from config import WINDOW_WIDTH, WINDOW_HEIGHT


# Camera
# camera = Camera(width=500, height=500)
camera = Camera.CURRENT_CAMERA
camera.d_w = 1
camera.d_h = 1

# Wall
wall = GameObj()
TransformComponent(wall, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)


# PLayer
player = GameObj()
TransformComponent(player, 15, 15, 100, 100)
SpriteComponent(player, 'media/sprites/fsociety.jpg')
ColliderComponent(player)
# AudioComponent(player, 'media/audio/toin.mp3')

# Fire
money = GameObj()
TransformComponent(money, width=100, height=100)
AnimationComponent(money, (
	'media/sprites/fire/frames/0.png',
	'media/sprites/fire/frames/1.png',
	'media/sprites/fire/frames/2.png',
	'media/sprites/fire/frames/3.png',
	'media/sprites/fire/frames/4.png',
	'media/sprites/fire/frames/5.png',
	), speed=0.25)

# Post-Processing
post_processing = GameObj()
TransformComponent(post_processing, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
AnimationComponent(post_processing, (
	'media/sprites/post_processing/1.png',
	'media/sprites/post_processing/2.png',
	'media/sprites/post_processing/3.png',
	'media/sprites/post_processing/4.png',
), speed=0.2)