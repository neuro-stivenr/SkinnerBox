import pygame
from graphics import COLOR_black, COLOR_red, COLOR_green, COLOR_white

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
        if len(schedules) > 9:
            raise Exception('Number of schedules greater than 9 is not implemented.')
        self.t = t * 1000
        self.schedules = schedules
        self.keymap = {k: i for i,k in enumerate(numeric_keys) if i < len(self.schedules)}
        self.colormap = [COLOR_black for _ in range(len(self.schedules))]
        self.score_color = COLOR_black
        self.score = 0

    def press(self, key:int):
        """
        Handles a keypress from pygame.
        """
        if key in self.keymap.keys():
            chosen_option = self.keymap[key]
            earned_point = self.schedules[chosen_option].press()
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

    def __len__(self):
        """
        Return the number of schedules designated in this trial.
        """
        return len(self.schedules)