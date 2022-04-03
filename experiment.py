import pygame
import pandas as pd
import numpy as np
from numpy.random import shuffle
from typing import List, Tuple
from schedules import ProbRatioBlock
from graphics import COLOR_black, COLOR_red, COLOR_green, COLOR_white
from graphics import draw_text, draw_option, draw_timer, draw_score
from graphics import circle_coords

def calc_score_ratio(df_log:pd.DataFrame):
    dist = df_log.press.value_counts()
    dominant_option = dist.argmax()
    distlist = dist.tolist()
    dominant_score = distlist.pop(dominant_option)
    others_score = np.sum(distlist)
    score_ratio = dominant_score / (others_score+1e-5)
    return score_ratio

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
        self.output = {
            'time': [],
            'press': [],
            'outcome': []
        }

    def press(self, key:int):
        """
        Handles a keypress from pygame.
        """
        if key in self.keymap.keys():
            chosen_option = self.keymap[key]
            chosen_schedule = self.schedules[chosen_option]
            earned_point = chosen_schedule.press()
            self.output['time'].append(self.t_elapsed / 1000)
            self.output['press'].append(chosen_option+1)
            self.output['outcome'].append(earned_point)
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
        return pd.DataFrame(self.output)
        
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

class DynamicProbTrial(Trial):
    def __init__(
        self, 
        ratiolist:List[float], 
        t:int, 
        shift_limit:int=3,
        warmup:int=50,
        inequality_threshold:float = 3.0
    ):
        schedules = ProbRatioBlock(ratiolist)
        super().__init__(schedules, t)
        self.ratiolist = ratiolist
        self.schedule_history = [[schedule.p for schedule in schedules]]
        self.shift_history = [0]
        self.shift_limit = shift_limit
        self.warmup_size = warmup
        self.warmup = warmup
        self.inequality_threshold = inequality_threshold
    def shuffle_contingencies(self):
        arr_schedules = np.array([schedule.p for schedule in self.schedules])
        best_option = arr_schedules.max()
        best_option_index = arr_schedules.argmax()
        while self.schedules[best_option_index].p == best_option:
            self.schedules = ProbRatioBlock(self.ratiolist)
    def press(self, key:int):
        super(DynamicProbTrial, self).press(key)
        # TODO: uncomment and indent next block
        if self.warmup > 0:
            self.warmup -= 1
        if (len(self.shift_history)-1) < self.shift_limit and self.warmup == 0:
            df_log = pd.DataFrame(self.output)
            df_log = df_log[df_log.time > self.shift_history[-1]]
            score_ratio = calc_score_ratio(df_log)
            print(score_ratio)
            if score_ratio > self.inequality_threshold:
                print(f"SHIFT: {self.t_elapsed / 1000}")
                self.shuffle_contingencies()
                self.schedule_history.append([schedule.p for schedule in self.schedules])
                self.shift_history.append(self.t_elapsed / 1000)
                self.warmup = self.warmup_size

class Message:
    # TODO: Add support foor multiline messages.
    def __init__(self, text:str):
        self.text = text

# --- DESIGN ---

class Design:

    def __init__(
        self, 
        design:List[Trial],
        screen_dims:Tuple[int,int] = (800,800),
        circle_radius:int = 300,
        show_timer:bool = False
    ):
        self.design = design
        self.circle_radius = circle_radius
        self.screen_dims = screen_dims
        self.screen_center = (screen_dims[0]/2, screen_dims[1]/2)
        self.screen = pygame.display.set_mode(screen_dims)
        self.show_timer = show_timer

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
                        *self.screen_center,
                        block.text
                    )
                    pygame.display.flip()

            # Handling Trial blocks
            elif issubclass(type(block), Trial):
                schedule_coords = circle_coords(
                    *self.screen_center,
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
                        *self.screen_center,
                        block.score, score_color=block.score_color
                    )
                    if self.show_timer:
                        draw_timer(
                            self.screen, 
                            self.screen_center[0], 
                            (self.screen_dims[1] / 2) + 50, 
                            block.t
                        )

                    pygame.display.flip()
                    tdelta = clock.tick(30)
                    done = block.tick(tdelta)

        self.write_output('Steve')



