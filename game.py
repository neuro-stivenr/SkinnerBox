import pygame
from math import sqrt
from schedules import FixedRatio
from graphics import draw_option, COLOR_black, COLOR_white, circle_coords

pygame.init()

screen_width, screen_height = 800, 800
screen_diagonal = sqrt(screen_width**2 + screen_height**2)
schedule_coords = list(circle_coords(
    center_x = screen_width / 2, 
    center_y = screen_height / 2,
    r = screen_diagonal / 4,
    n = 10
))
circle_radius = screen_diagonal / 4

screen = pygame.display.set_mode((screen_width, screen_height))

schedule_coords = circle_coords(
    center_x = 400, 
    center_y = 400,
    r = 300,
    n = 3
)

running = True
while running:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # game logic
    
    # rendering business
    screen.fill(COLOR_white)

    for i, (x,y) in enumerate(schedule_coords):
        draw_option(screen, x, y, i)

    pygame.display.update()

pygame.quit()
