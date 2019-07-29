import math
import os
from random import randint
from collections import deque
import pygame
from pygame.locals import *

#variables
FPS = 60
ANIMATION_SPEED = .18
WIN_WIDTH = 284*2
WIN_HEIGHT = 512

class Bird(pygame.sprite.Sprite):

    WIDTH = HEIGHT = 32
    SINK_SPEED = .18
    CLIMB_SPEED = .3
    CLIMB_DURATION = 333.3

    def __init__(self,x,y,msec_to_climb,images):

        super(Bird,self).__init__()
        self.x, self.y = x,y

        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frame=1):
        # number of frames ellapsed
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION

            self.y -= (Bird.CLIMB_SPEED*frames_to_msec(delta_frame))*(1-math.cos(frac_climb_done*math.pi))
            self.msec_to_climb -= frames_to_msec(delta_frame)

        else:
            self.y += Bird.SINK_SPEED*frames_to_msec(delta_frame)

    @property
    def image(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @@property
    def rect(self):
        return Rect(self.x,self.y,Bird.WIDTH,Bird.HEIGHT)

    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown



def load_images():

    def load_image(img_file_name):

        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'background': load_image('background.png'),
            'pipe-end': load_image('pipe_end.png'),
            'pipe-body': load_image('pipe_body.png'),
            'bird-wingup': load_image('bird_wing_up.png'),
            'bird-wingdown': load_image('bird_wing_down.png')}

def frames_to_msec(frame, fps=FPS):
    return 1000.0 * frame / fps

def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0

def main():
    pygame.init()
    display_surface = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    score_font = pygame.font.SysFont(None, 32, bold=True)

    images = load_images()