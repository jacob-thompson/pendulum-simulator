from os import path
from sys import exit

import pygame

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Pendulum Simulator"
FPS = 60

class Pendulum:
    def __init__(self):
        pygame.display.init()
        self.surface = pygame.display.set_mode(SCREEN_SIZE)

        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.dir, self.file = path.split(__file__)
        font_file = path.join(self.dir, "data", "font.otf")
        self.font = pygame.font.Font(font_file, 12)
        self.bigfont = pygame.font.Font(font_file, 20)

        self.active = False

        self.mouse = self.mousex, self.mousey = 0, 0
        self.mouseb = (False, False, False)

        self.pivot_pos = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 2
        self.pivot_radius = 12

        self.bob_pos = SCREEN_WIDTH >> 1, SCREEN_HEIGHT - (SCREEN_HEIGHT >> 2)
        self.bob_radius = 27

        self.rod_width = 3

        self.selected_rect = pygame.Rect(0, 0, 0, 0)
        self.selected = None

        self.grabbed = False

    def set_window_properties(self):
        pygame.display.set_caption(TITLE)

        icon_file = path.join(self.dir, "data", "logo.png")
        icon = pygame.image.load(icon_file)
        pygame.display.set_icon(icon)

    def print_info(self):
        print(f"{TITLE} https://github.com/jacob-thompson/pendulum-simulator")

    def tick(self):
        self.clock.tick(FPS)

    def handle_event(self, event):
        if event.type == pygame.QUIT: exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: exit()
            else: self.active = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = True

    def handle_mouse(self):
        self.mouse = self.mousex, self.mousey = pygame.mouse.get_pos()
        self.mouseb = pygame.mouse.get_pressed()

        pivot = pygame.Rect(0, 0, self.pivot_radius << 1, self.pivot_radius << 1)
        pivot.center = self.pivot_pos

        bob = pygame.Rect(0, 0, self.bob_radius << 1, self.bob_radius << 1)
        bob.center = self.bob_pos

        rod = pygame.draw.line(self.surface, BLACK, self.pivot_pos, self.bob_pos, self.rod_width << 1)

        #button == 1 is mouse1; left click
        #button == 2 is scroll wheel; middle click
        #button == 3 is mouse2; right click

        if pivot.collidepoint(self.mouse) and self.mouseb[2]:
            self.selected_rect = pivot.copy()
            self.selected = "frictionless pivot"
        elif bob.collidepoint(self.mouse) and (self.mouseb[0] or self.mouseb[2]):
            self.selected_rect = bob.copy()
            self.selected = "massive bob"
        elif rod.collidepoint(self.mouse) and self.mouseb[2]:
            self.selected_rect = rod.copy()
            self.selected = "massless rod"
        elif self.mouseb[2]: self.selected = None

        if bob.collidepoint(self.mouse) and self.mouseb[0]: self.grabbed = True
        elif self.mouseb[0]: self.selected = None
        else: self.grabbed = False

        #print(self.grabbed)

    def draw_background(self):
        self.surface.fill(WHITE)

    def draw_pivot(self):
        pygame.draw.circle(self.surface, BLACK, self.pivot_pos, self.pivot_radius)

    def draw_bob(self):
        pygame.draw.circle(self.surface, BLACK, self.bob_pos, self.bob_radius + 1)
        pygame.draw.circle(self.surface, WHITE, self.bob_pos, self.bob_radius)

    def draw_rod(self):
        pygame.draw.line(self.surface, BLACK, self.pivot_pos, self.bob_pos, self.rod_width)

    def draw_selected(self):
        if self.selected == None: pass
        elif self.selected == "frictionless pivot":
            position = f"position: {self.selected_rect.center}"
            position_surface = self.bigfont.render(position, 1, BLACK)
            position_pos = SCREEN_WIDTH - 3, SCREEN_HEIGHT
            position_rect = position_surface.get_rect(bottomright = position_pos)
            self.surface.blit(position_surface, position_rect)

            name_surface = self.bigfont.render(self.selected, 1, BLACK)
            name_pos = position_rect.topright
            name_rect = name_surface.get_rect(bottomright = name_pos)
            self.surface.blit(name_surface, name_rect)
        elif self.selected == "massive bob":
            position = f"position: {self.selected_rect.center}"
            position_surface = self.bigfont.render(position, 1, BLACK)
            position_pos = SCREEN_WIDTH - 3, SCREEN_HEIGHT
            position_rect = position_surface.get_rect(bottomright = position_pos)
            self.surface.blit(position_surface, position_rect)

            name_surface = self.bigfont.render(self.selected, 1, BLACK)
            name_pos = position_rect.topright
            name_rect = name_surface.get_rect(bottomright = name_pos)
            self.surface.blit(name_surface, name_rect)
        elif self.selected == "massless rod":
            end = f"end point: {self.selected_rect.midbottom}"
            end_surface = self.bigfont.render(end, 1, BLACK)
            end_pos = SCREEN_WIDTH - 3, SCREEN_HEIGHT
            end_rect = end_surface.get_rect(bottomright = end_pos)
            self.surface.blit(end_surface, end_rect)

            start = f"start point: {self.selected_rect.midtop}"
            start_surface = self.bigfont.render(start, 1, BLACK)
            start_pos = end_rect.topright
            start_rect = start_surface.get_rect(bottomright = start_pos)
            self.surface.blit(start_surface, start_rect)

            name_surface = self.bigfont.render(self.selected, 1, BLACK)
            name_pos = start_rect.topright
            name_rect = name_surface.get_rect(bottomright = name_pos)
            self.surface.blit(name_surface, name_rect)

    def draw_pendulum(self):
        self.draw_pivot()
        self.draw_rod()
        self.draw_bob() # must be drawn after rod

    def draw_license_disclaimer(self):
        disclaimer = "MIT License Copyright (c) 2023 Jacob Alexander Thompson"
        surface = self.font.render(disclaimer, 1, BLACK)
        pos = 3, SCREEN_HEIGHT
        rect = surface.get_rect(bottomleft = pos)
        self.surface.blit(surface, rect)

    def draw_frame(self):
        self.draw_background()

        self.draw_selected()

        self.draw_pendulum()

        if not self.active:
            self.draw_license_disclaimer()

    def update_frame(self):
        pygame.display.flip()