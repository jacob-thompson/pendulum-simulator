from .cfg import SCREEN_W, SCREEN_H, TITLE, FPS

from sys import exit

import pygame

class Pendulum:
    def __init__(self):
        pygame.display.init()

        size = SCREEN_W, SCREEN_H
        self.surface = pygame.display.set_mode(size)

        self.clock = pygame.time.Clock()

        # font here

        # sounds here if any

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)

    def set_window_properties(self):
        pygame.display.set_caption(TITLE)

        # icon here

    def print_info(self):
        print("pendulum-simulator : https://github.com/jacob-thompson/pendulum-simulator")

    def tick(self):
        self.clock.tick(FPS)

    def handle_event(self, event):
        if event.type == pygame.QUIT: exit()

    def draw_background(self):
        self.surface.fill(self.white)

    def draw_frame(self):
        self.draw_background()

    def update_frame(self):
        pygame.display.flip()