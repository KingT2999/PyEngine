import pygame
import random
from engine.scripts import *
from config import *
from models import *
from engine.components import *


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
	camera.follow((player.transform.x + player.transform.width // 2, player.transform.y + player.transform.height // 2), WINDOW_WIDTH, WINDOW_HEIGHT)

# 
@PreRenderUpdate
def player_money_pre_render() -> None:
	for money in money_list:
		if player.collider.is_intersection(money):
			money_list.remove(money)

@RenderUpdate
def wall_render(screen) -> None:
	pygame.draw.rect(screen, (0, 0, 0), (camera.get_local_x(wall.transform.x), camera.get_local_y(wall.transform.y), wall.transform.width, wall.transform.height), 5)

@RenderUpdate
def money_render(screen) -> None:
	for money in money_list:
		money.sprite.render_to(screen, camera.get_local_coords(money.transform.get_coords()))
		money.sprite.anim_play()

@RenderUpdate
def player_render(screen) -> None:
	player.sprite.render_to(screen, camera.get_local_coords(player.transform.get_coords()))