import pygame
import random
from engine.scripts import *
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from models import *
from engine.components import *


@Start
def music_start():
	pygame.mixer.music.load('media/audio/music.mp3')
	pygame.mixer.music.play(loops=1)

@Start
def player_start() -> None:
	player.speed = 5

@Start
def money_spawn() -> None:
	global money_list

	money_list = []

	for i in range(5):
		m = money.spawn()
		m.transform.x = random.randint(0, 400)
		m.transform.y = random.randint(0, 400)

		money_list.append(m)

@PreRenderUpdate
def camera_pre_render_update() -> None:
	if 100 == camera.width or camera.width == 1000:
		camera.d_w = -camera.d_w
	if 100 == camera.height or camera.height == 1000:
		camera.d_h = -camera.d_h
	
	camera.width += camera.d_w
	camera.height += camera.d_h

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
	for money in money_list:
		if player.collider.is_intersection(money):
			money_list.remove(money)

# Screen Fill
@RenderUpdate
def screen_fill_render(screen) -> None:
    screen.fill((64, 64, 64))

# Wall
@RenderUpdate
def wall_render(screen) -> None:
	pygame.draw.rect(screen, (0, 0, 0), (camera.get_local_x(wall.transform.x), camera.get_local_y(wall.transform.y),
	wall.transform.width * camera.width_coeff, wall.transform.height * camera.height_coeff), 5)

# Money
@RenderUpdate
def money_render(screen) -> None:
	for money in money_list:
		money.sprite.render(screen)
		money.sprite.anim_play()

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