import pygame
import random
from engine.scripts import *
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from models import *
from engine.components import *


@Start
def music_start():
	pygame.mixer.music.load('media/audio/music.mp3')
	pygame.mixer.music.play(loops=-1)

	pygame.mixer.music.set_volume(0.25)

@Start
def player_start() -> None:
	player.speed = 5

@Start
def fire_spawn() -> None:
	global fire_list

	fire_list = []

	for i in range(5):
		f = fire.spawn()
		f.transform.x = random.randint(0, 400)
		f.transform.y = random.randint(0, 400)

		fire_list.append(f)

@PreRenderUpdate
def fire_pre_render() -> None:
	if len(fire_list) < 5:
		f = fire.spawn()
		f.transform.x = random.randint(0, 400)
		f.transform.y = random.randint(0, 400)
		fire_list.append(f)

	speed = 2
	for f in fire_list:
		if player.transform.x < f.transform.x:
			f.transform.x -= speed
		else:
			f.transform.x += speed
		
		if player.transform.y < f.transform.y:
			f.transform.y -= speed
		else:
			f.transform.y += speed

# @PreRenderUpdate
# def bullet_pre_render():
# 	global bullet_list

# 	bullet_list = []

# 	if pygame.mouse.get_pressed(3):
# 		b = bullet.spawn()
# 		b.transform.x = player.transform.x
# 		b.transform.y = player.transform.y


# 		bullet_list.append(b)

# Player Move
@PreRenderUpdate
def player_pre_render() -> None:
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w] or keys[pygame.K_UP]:
		if player.transform.y > 0:
			player.transform.y -= player.speed
	elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
		if player.transform.y < WINDOW_HEIGHT - player.transform.height:
			player.transform.y += player.speed

	if keys[pygame.K_a] or keys[pygame.K_LEFT]:
		if player.transform.x > 0:
			player.transform.x -= player.speed
	elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
		if player.transform.x < WINDOW_WIDTH - player.transform.height:
			player.transform.x += player.speed

	# Camera Follow
	camera.follow((player.transform.x + player.transform.width // 2, player.transform.y + player.transform.height // 2))

# player and fire intersection
@PreRenderUpdate
def player_money_pre_render() -> None:
	for fire in fire_list:
		if player.collider.is_intersection(fire):
			fire_list.remove(fire)

# Screen Fill
@RenderUpdate
def screen_fill_render(screen) -> None:
    screen.fill((84, 0, 0))

# Wall
@RenderUpdate
def wall_render(screen) -> None:
	pygame.draw.rect(screen, (0, 0, 0), (camera.get_local_x(wall.transform.x), camera.get_local_y(wall.transform.y),
	wall.transform.width * camera.width_coeff, wall.transform.height * camera.height_coeff), 5)

# Money
@RenderUpdate
def fire_render(screen) -> None:
	for fire in fire_list:
		fire.sprite.render(screen)
		fire.sprite.anim_play()

# Plyaer
@RenderUpdate
def player_render(screen) -> None:
	player.sprite.render(screen)

# Post-Processing
@RenderUpdate
def post_processing_render(screen) -> None:
	post_processing.transform.x = camera.x
	post_processing.transform.y = camera.y
	post_processing.transform.width = camera.width
	post_processing.transform.height = camera.height

	post_processing.sprite.render(screen)
	post_processing.sprite.anim_play()