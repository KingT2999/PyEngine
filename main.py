import pygame
from config import *
from engine.scripts import *
import scripts


pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Engine')

# Start Scripts Activate
for script in START_SCRIPTS:
    script()

clock = pygame.time.Clock()
while True:
    # Update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        for script in UPDATE_SCRIPTS:
            script(event)


    for script in PRE_RENDER_UPDATE_SCRIPTS:
        script()

    # Render
    screen.fill((0, 255, 0))

    for script in RENDER_UPDATE_SCRIPTS:
        script(screen)

    pygame.display.update()

    # FPS
    pygame.display.set_caption(f'My Engine | FPS:{int(clock.get_fps())}')
    clock.tick(FPS)