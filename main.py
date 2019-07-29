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

    @property
    def rect(self):
        return Rect(self.x,self.y,Bird.WIDTH,Bird.HEIGHT)

    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

class PipePair(pygame.sprite.Sprite):
    #obstacle for the bird
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img,pipe_body_img):
        self.x = float(WIN_WIDTH-1)
        self.score_counted = False
        self.image = pygame((PipePair.WIDTH.WIN_HEIGHT),SRCALPHA)
        self.image.convert()
        self.image.fill((0,0,0))

        total_pipe_pieces = int((WIN_HEIGHT-
                                 3*WIN_HEIGHT-
                                 3*PipePair.PIECE_HEIGHT)/
                                 PipePair.PIECE_HEIGHT

                                 )
        self.bottom_pieces = randint(1,total_pipe_pieces)
        self.top_pieces = randint(1,total_pipe_pieces)

        for i in range(1,self.bottom_pieces+1):
            piece_pos = (0,WIN_HEIGHT-i*PipePair.PIECE_HEIGHT)

            self.image.blit(pipe_body_img,piece_pos)


        bottom_pipe_end_y = WIN_HEIGHT-self.bottom_height_px
        bottom_end_pipe_pos = (0,bottom_pipe_end_y - PipePair.PIECE_HEIGHT)

        self.image.blit(pipe_end_img, bottom_end_pipe_pos)

        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img,(0,i*PipePair*PIECE_HEIGHT))

        total_pipe_end_x = self.top_height_px
        self.image.blit(pipe_end_img,(0,total_pipe_end_x))

        self.top_pieces += 1
        self.bottom_pieces += 1

        # detect collision

        self.mask = pygame.mask.from_surface(self.image)









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