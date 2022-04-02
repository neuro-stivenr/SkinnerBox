import pygame
import pandas as pd
from typing import List, Tuple
from graphics import COLOR_black, COLOR_red, COLOR_green, COLOR_white
from graphics import draw_text, draw_option, draw_timer, draw_score
from graphics import circle_coords

pygame.init()

numeric_keys = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9
]

class Trial:

    def __init__(self, schedules:list, t:int):
        global numeric_keys
        self.schedules = schedules
        if len(schedules) > 9:
            raise Exception('Number of schedules greater than 9 is not implemented.')
        # timekeeping
        self.t = t * 1000
        self.tmax = t * 1000
        self.t_elapsed = 0
        # game related aspects
        self.keymap = {k: i for i,k in enumerate(numeric_keys) if i < len(self.schedules)}
        self.colormap = [COLOR_black for _ in range(len(self.schedules))]
        self.score_color = COLOR_black
        # scorekeeping
        self.score = 0
        # for data output
        self.timestamp = []
        self.presslog = []
        self.outcomelog = []

    def press(self, key:int):
        """
        Handles a keypress from pygame.
        """
        if key in self.keymap.keys():
            chosen_option = self.keymap[key]
            chosen_schedule = self.schedules[chosen_option]
            earned_point = chosen_schedule.press()
            self.timestamp.append(self.t_elapsed)
            self.presslog.append(chosen_option+1)
            self.outcomelog.append(earned_point)
            if earned_point:
                self.colormap[chosen_option] = COLOR_green
                self.score_color = COLOR_green
                self.score += 1
            else:
                self.colormap[chosen_option] = COLOR_red

    def tick(self, time:int):
        """
        Decrements the amount of time remaining in the trial.
        """
        self.t -= time
        self.t_elapsed += time
        if self.t <= 0:
            return True
        else:
            return False

    def reset_colormap(self):
        """
        Resets the colors of option circles.
        """
        self.colormap = [COLOR_black for _ in range(len(self.schedules))]

    def reset_score_color(self):
        """
        Resets the color of the score.
        """
        self.score_color = COLOR_black

    def return_log(self):
        return pd.DataFrame({
            'time': self.timestamp,
            'press': self.presslog,
            'outcome': self.outcomelog
        })

    def return_schedules(self):
        return pd.DataFrame({
            'schedule': [i+1 for i in range(len(self.schedules))],
            'p': [schedule.p for schedule in self.schedules]
        })

    def __len__(self):
        """
        Return the number of schedules designated in this trial.
        """
        return len(self.schedules)

class Message:

    def __init__(self, text:str):
        self.text = text

class Design:

    def __init__(
        self, 
        design:List[Trial],
        screen_dims:Tuple[int,int] = (800,800),
        circle_radius:int = 300
    ):
        self.design = design
        self.circle_radius = circle_radius
        self.screen_dims = screen_dims
        self.screen = pygame.display.set_mode(screen_dims)

    def write_output(self, prefix:str='Subject'):
        for i,trial in enumerate(filter(
            lambda block: type(block) == Trial,
            self.design
        )):
            trial.return_log().to_csv(f'{prefix}_trial-{i+1}_log.csv', index=False)
            trial.return_schedules().to_csv(f'{prefix}_trial-{i+1}_schedules.csv', index=False)

    def run(self):
        for block in self.design:

            # Handling Message blocks
            if type(block) == Message:
                done = False
                while not done:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            done = True
                    self.screen.fill(COLOR_white)
                    draw_text(
                        self.screen,
                        self.screen_dims[0] / 2,
                        self.screen_dims[1] / 2,
                        block.text
                    )
                    pygame.display.flip()

            # Handling Trial blocks
            elif type(block) == Trial:
                schedule_coords = circle_coords(
                    center_x = self.screen_dims[0] / 2, 
                    center_y = self.screen_dims[1] / 2,
                    r = self.circle_radius,
                    n = len(block)
                )
                clock = pygame.time.Clock()
                done = False
                while not done:
                    block.reset_colormap()
                    block.reset_score_color()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
                        if event.type == pygame.KEYDOWN:
                            block.press(event.key)
                    if done: break
                    self.screen.fill(COLOR_white)

                    for i, (x,y) in enumerate(schedule_coords):
                        draw_option(
                            self.screen, x, y,
                            i, circle_color=block.colormap[i]
                        )

                    draw_score(
                        self.screen,
                        self.screen_dims[0] / 2, 
                        self.screen_dims[1] / 2, 
                        block.score, score_color=block.score_color
                    )

                    draw_timer(
                        self.screen, 
                        self.screen_dims[0] / 2, 
                        (self.screen_dims[1] / 2) + 50, 
                        block.t
                    )

                    pygame.display.flip()
                    tdelta = clock.tick()
                    done = block.tick(tdelta)

        self.write_output('Steve')



