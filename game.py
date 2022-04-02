import pygame
from math import sqrt
from schedules import FixedRatio, ProbRatio, ProbRatioBlock
from graphics import draw_score, draw_option, draw_timer, circle_coords
from graphics import COLOR_black, COLOR_white, COLOR_red, COLOR_green
from Trial import Trial

pygame.init()

screen_width, screen_height = 800, 800
screen_diagonal = sqrt(screen_width**2 + screen_height**2)
screen = pygame.display.set_mode((screen_width, screen_height))

# Trial being defined

trial = Trial(
    ProbRatioBlock([0.1, 0.15, 0.2, 0.25, 0.3]),
    t=90
)

schedule_coords = circle_coords(
    center_x = 400, 
    center_y = 400,
    r = 300,
    n = len(trial)
)

done = False
clock = pygame.time.Clock()

while not done:

    trial.reset_colormap()
    trial.reset_score_color()

    # event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            earned_point = trial.press(event.key)
    
    # rendering business
    screen.fill(COLOR_white)

    for i, (x,y) in enumerate(schedule_coords):
        draw_option(screen, x, y, i, circle_color=trial.colormap[i])
        draw_score(screen, 400, 400, trial.score, score_color=trial.score_color)
        draw_timer(screen, 400, 350, trial.t)

    pygame.display.update()
    tdelta = clock.tick()
    done = trial.tick(tdelta)

print('\nPoints earned: ' + str(trial.score))
for i, schedule in enumerate(trial.schedules):
    print(f'Ratio {i+1} [{schedule.p}]: {schedule.counter}')

pygame.quit()
