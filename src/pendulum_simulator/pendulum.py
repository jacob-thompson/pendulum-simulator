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
        font_file = path.join(self.dir, "data", "font.otf")
        self.font = pygame.font.Font(font_file, 12)
        self.font_big = pygame.font.Font(font_file, 20)

        self.blk = pygame.Color(0, 0, 0)
        self.wht = pygame.Color(255, 255, 255)

        self.in_use = False

        self.pivot_pos = SCREEN_W >> 1, SCREEN_H >> 2
        self.pivot_r = 12

        self.bob_pos = SCREEN_W >> 1, SCREEN_H - (SCREEN_H >> 2)
        self.bob_r = 27

        self.rod_w = 3

        self.selected_rect = pygame.Rect(0, 0, 0, 0)
        self.selected = None

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
        self.in_use = True

        pivot_dimension = self.pivot_r << 1
        pivot_hitbox = pygame.Rect(0, 0, pivot_dimension, pivot_dimension)
        pivot_hitbox.center = self.pivot_pos

        bob_dimension = self.bob_r << 1
        bob_hitbox = pygame.Rect(0, 0, bob_dimension, bob_dimension)
        bob_hitbox.center = self.bob_pos

        rod_hitbox = pygame.draw.line(self.surface, self.blk, self.pivot_pos, self.bob_pos, self.rod_w << 1)

        #button == 1 is mouse1; left click
        #button == 2 is scroll wheel; middle click
        #button == 3 is mouse2; right click

        if pivot_hitbox.collidepoint(pos) and button == 3:
            self.selected_rect = pivot_hitbox.copy()
            self.selected = "frictionless pivot"
        elif bob_hitbox.collidepoint(pos) and button == 3:
            self.selected_rect = bob_hitbox.copy()
            self.selected = "massive bob"
        elif rod_hitbox.collidepoint(pos) and button == 3:
            self.selected_rect = rod_hitbox.copy()
            self.selected = "massless rod"
        else: self.selected = None

    def draw_background(self):
        self.surface.fill(self.wht)

    def draw_pivot(self):
        pygame.draw.circle(self.surface, self.blk, self.pivot_pos, self.pivot_r)

    def draw_bob(self):
        pygame.draw.circle(self.surface, self.blk, self.bob_pos, self.bob_r + 1)
        pygame.draw.circle(self.surface, self.wht, self.bob_pos, self.bob_r)

    def draw_rod(self):
        pygame.draw.line(self.surface, self.blk, self.pivot_pos, self.bob_pos, self.rod_w)

    def draw_selected(self):
        if self.selected == None: pass
        elif self.selected == "frictionless pivot":
            position = f"position: {self.selected_rect.center}"
            position_surface = self.font_big.render(position, 1, self.blk)
            position_pos = SCREEN_W - 3, SCREEN_H
            position_rect = position_surface.get_rect(bottomright = position_pos)
            self.surface.blit(position_surface, position_rect)

            name_surface = self.font_big.render(self.selected, 1, self.blk)
            name_pos = position_rect.topright
            name_rect = name_surface.get_rect(bottomright = name_pos)
            self.surface.blit(name_surface, name_rect)
        elif self.selected == "massive bob":
            position = f"position: {self.selected_rect.center}"
            position_surface = self.font_big.render(position, 1, self.blk)
            position_pos = SCREEN_W - 3, SCREEN_H
            position_rect = position_surface.get_rect(bottomright = position_pos)
            self.surface.blit(position_surface, position_rect)

            name_surface = self.font_big.render(self.selected, 1, self.blk)
            name_pos = position_rect.topright
            name_rect = name_surface.get_rect(bottomright = name_pos)
            self.surface.blit(name_surface, name_rect)
        elif self.selected == "massless rod":
            end = f"end point: {self.selected_rect.midbottom}"
            end_surface = self.font_big.render(end, 1, self.blk)
            end_pos = SCREEN_W - 3, SCREEN_H
            end_rect = end_surface.get_rect(bottomright = end_pos)
            self.surface.blit(end_surface, end_rect)

            start = f"start point: {self.selected_rect.midtop}"
            start_surface = self.font_big.render(start, 1, self.blk)
            start_pos = end_rect.topright
            start_rect = start_surface.get_rect(bottomright = start_pos)
            self.surface.blit(start_surface, start_rect)

            name_surface = self.font_big.render(self.selected, 1, self.blk)
            name_pos = start_rect.topright
            name_rect = name_surface.get_rect(bottomright = name_pos)
            self.surface.blit(name_surface, name_rect)

    def draw_pendulum(self):
        self.draw_pivot()
        self.draw_rod()
        self.draw_bob() # must be drawn after rod

    def draw_info(self):
        info = "MIT License Copyright (c) 2023 Jacob Alexander Thompson"
        text_surface = self.font.render(info, 1, self.blk)
        text_pos = 3, SCREEN_H
        text_rect = text_surface.get_rect(bottomleft = text_pos)
        self.surface.blit(text_surface, text_rect)

    def draw_frame(self):
        self.draw_background()

        self.draw_selected()

        self.draw_pendulum()

        if not self.in_use:
            self.draw_info()

    def update_frame(self):
        pygame.display.flip()