from .cfg import SCREEN_W, SCREEN_H, TITLE, FPS

from os import path
from sys import exit

import pygame

class Pendulum:
    def __init__(self):
        pygame.display.init()

        size = SCREEN_W, SCREEN_H
        self.surface = pygame.display.set_mode(size)

        self.clock = pygame.time.Clock()

        self.dir, self.file = path.split(__file__)

        pygame.font.init()
        font_file = path.join(self.dir, "data", "placeholder.otf")
        self.font = pygame.font.Font(font_file, 10)

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)

        self.in_use = False

        self.pivot = SCREEN_W >> 1, 100
        self.pivot_radius = 7

        self.bob = SCREEN_W >> 1, (SCREEN_H >> 1) + 100
        self.bob_radius = 20

    def set_window_properties(self):
        pygame.display.set_caption(TITLE)

        icon_file = path.join(self.dir, "data", "logo.png")
        icon = pygame.image.load(icon_file)
        pygame.display.set_icon(icon)

    def print_info(self):
        print("pendulum-simulator https://github.com/jacob-thompson/pendulum-simulator")

    def tick(self):
        self.clock.tick(FPS)

    def handle_event(self, event):
        if event.type == pygame.QUIT: exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.interact(event.pos, event.button)

    def interact(self, pos, button):
        pivot_dimension = self.pivot_radius << 1
        pivot_hitbox = pygame.Rect(0, 0, pivot_dimension, pivot_dimension)
        pivot_hitbox.center = self.pivot

        bob_dimension = self.bob_radius << 1
        bob_hitbox = pygame.Rect(0, 0, bob_dimension, bob_dimension)
        bob_hitbox.center = self.bob

        self.in_use = True

        #button == 1 is mouse1
        #button == 2 is scroll wheel
        #button == 3 is mouse2

        if pivot_hitbox.collidepoint(pos) and button == 1: self.select_pivot()
        if bob_hitbox.collidepoint(pos) and button == 1: self.select_bob()

    def select_pivot(self):
        print("frictionless pivot")
        print(f"position: {self.pivot}")
        print(f"radius: {self.pivot_radius}")

    def select_bob(self):
        print("massive bob")
        print(f"position: {self.bob}")
        print(f"radius: {self.bob_radius}")

    def draw_background(self):
        self.surface.fill(self.white)

    def draw_info(self):
        info = "MIT License Copyright (c) 2023 Jacob Alexander Thompson"

        dtext = self.font.render(info, 1, self.black)
        dtpos = 3, SCREEN_H
        dtrect = dtext.get_rect(bottomleft = dtpos)
        self.surface.blit(dtext, dtrect)

    def draw_pivot(self):
        pygame.draw.circle(self.surface, self.black, self.pivot, self.pivot_radius)

    def draw_bob(self):
        pygame.draw.circle(self.surface, self.black, self.bob, self.bob_radius, 1)

    def draw_frame(self):
        self.draw_background()
        self.draw_pivot()
        self.draw_bob()

        if not self.in_use:
            self.draw_info()

    def update_frame(self):
        pygame.display.flip()