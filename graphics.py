import pygame
from pygame.locals import *
from datetime import timedelta
import numpy as np

pygame.font.init()

default_font = pygame.font.Font('freesansbold.ttf', 32)
score_font = pygame.font.Font('freesansbold.ttf', 64)
option_font = pygame.font.Font('freesansbold.ttf', 32)

COLOR_white = (255,255,255)
COLOR_black = (0,0,0)
COLOR_red = (255,0,0)
COLOR_green = (0,255,0)

def draw_option(window, x:float, y:float, i:int, r:float=70, circle_color=COLOR_black):
    """
    Renders an option circle.
    """
    global font, COLOR_black, COLOR_white
    pygame.draw.circle(
        surface=window, 
        center=(x,y), 
        color=circle_color, 
        radius=r
    )
    pygame.draw.circle(
        surface=window, 
        center=(x,y), 
        color=COLOR_white, 
        radius=(r-20)
    )
    text = option_font.render(str(i+1), True, COLOR_black)
    text_rect = text.get_rect()
    text_rect.center = x, y
    window.blit(text, text_rect)

def draw_text(window, x:float, y:float, text:str, font=default_font, color=COLOR_black):
    rendered = font.render(text, True, color)
    render_rect = rendered.get_rect()
    render_rect.center = x, y
    window.blit(rendered, render_rect)

def draw_score(window, x:float, y:float, score:int, score_color=COLOR_black):
    global score_font
    score_string = str(score)
    draw_text(window, x, y, score_string, score_font, score_color)

def draw_timer(window, x:float, y:float, t:int):
    td = timedelta(milliseconds=t)
    seconds_string = str(td.total_seconds())
    draw_text(window, x, y, seconds_string)

def circle_coords(center_x:float, center_y:float, r:float, n:int, resolution:int=1000):
    """
    Given a center of the circle, it's radius, and number of points,
    gives coordinates of equidistant points along that circle.
    """
    resolution -= (resolution % n)
    theta = np.linspace(0, 2*np.pi, resolution) # start, stop, splits
    # r = np.sqrt(r) # radius
    x1 = r*np.cos(theta) + center_x # continuous range of x values
    x2 = r*np.sin(theta) + center_y # continuous range of y values
    x = np.array(np.split(x1, n))[:,0].tolist() # equidistant x coords
    y = np.array(np.split(x2, n))[:,0].tolist() # equidistant y coords
    return list(zip(x, y))
