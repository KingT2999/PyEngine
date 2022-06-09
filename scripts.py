import pygame
import random
from engine.scripts import *
from config import *
from models import *
from engine.components import *


@Start
def hacker_start():
	hacker.speed = 5

@Start
def money_spawn():
	global money_list

	money_list = []

	for i in range(5):
		money = GameObj()
		TransformComponent(money, x=random.randint(0, 400), y=random.randint(0, 400), width=100, height=100)
		SpriteComponent(money, 'media/sprites/money.png')

		money_list.append(money)

# Player Move
@PreRenderUpdate
def hacker_pre_render():
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w] or keys[pygame.K_UP]:
		if hacker.transform.y > 0:
			hacker.transform.y -= hacker.speed
	elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
		if hacker.transform.y < HEIGHT - hacker.transform.height:
			hacker.transform.y += hacker.speed

	if keys[pygame.K_a] or keys[pygame.K_LEFT]:
		if hacker.transform.x > 0:
			hacker.transform.x -= hacker.speed
	elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
		if hacker.transform.x < WIDTH - hacker.transform.height:
			hacker.transform.x += hacker.speed

	# Camera Follow
	camera.follow((hacker.transform.x + hacker.transform.width // 2, hacker.transform.y + hacker.transform.height // 2), WIDTH, HEIGHT)

# 
@PreRenderUpdate
def hacker_money_pre_render():
	for money in money_list:
		if hacker.collider.is_intersection(money):
			money_list.remove(money)

@RenderUpdate
def wall_render(screen):
	pygame.draw.rect(screen, (0, 0, 0), (camera.get_local_x(wall.transform.x), camera.get_local_y(wall.transform.y), wall.transform.width, wall.transform.height), 5)

@RenderUpdate
def money_render(screen):
	for money in money_list:
		money.sprite.render_to(screen, camera.get_local_coords(money.transform.get_coords()))

@RenderUpdate
def hacker_render(screen):
	hacker.sprite.render_to(screen, camera.get_local_coords(hacker.transform.get_coords()))