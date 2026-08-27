import random

import pygame
from pygame import math

import gameManager
from constants import screen_width, screen_height


class AnimationManager:
    def __init__(self):
        self.destination_rect = pygame.Rect((0, 0), (80, 20))
        self.destination_rect.center = (screen_width // 2, screen_height // 2)
        self.ongoing_animation = False

    def uranium_pellet_animations(self,num_pellets:int=100):
        self.ongoing_animation = True
        gameManager.money_desync = True
        self.pellets = [UraniumPelletAnimation((screen_width // 2, 100), 10, (screen_width // 2, screen_height//2))
                        for _ in range(num_pellets)]

    def render(self, win: pygame.Surface):
        if not self.ongoing_animation:
            return
        for pellet in self.pellets:
            if self.destination_rect.collidepoint(pellet.position):
                self.pellets.remove(pellet)
                del pellet
                gameManager.display_money += 1
                continue
            pellet.render(win)
            pellet.next_frame()
        if self.pellets == []:
            gameManager.money_desync = False
            gameManager.display_money = gameManager.money


class UraniumPelletAnimation:
    def __init__(self, position: tuple[int, int], size: int, destination: tuple[int, int]):
        self.start_position = position
        self.position = position
        self.destination = destination
        self.size = size
        self.current_frame = 0
        self.frame_to_reach_max_size = random.randint(10, 20)
        self.frame_to_reach_destination = random.randint(40, 100)
        self.bezier_control = self.calculate_bezier_p3(self.start_position, self.destination)

    def calculate_bezier_p3(self, start: tuple[int, int], end: tuple[int, int]):
        diff = (end[0] - start[0], end[1] - start[1])
        main_movement_axis = 0 if diff[0] > diff[1] else 1
        p3 = [start[0] + diff[0] // 2, start[1] + diff[1] // 2]
        p3[1 - main_movement_axis] += random.randint(-500, 500)
        return p3

    def bezier_curve(self, t: float):
        return ((1 - t) ** 2 * self.start_position[0] + 2 * (1 - t) * t * self.bezier_control[0] + t ** 2 *
                self.destination[0],
                (1 - t) ** 2 * self.start_position[1] + 2 * (1 - t) * t * self.bezier_control[1] + t ** 2 *
                self.destination[1])

    def next_frame(self):
        self.position = self.bezier_curve(self.current_frame / self.frame_to_reach_destination)
        self.current_frame += 1

    def render(self, win: pygame.Surface):
        pygame.draw.circle(win, "darkgreen", self.position, self.size)
