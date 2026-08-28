import random

import pygame
import math

import gameManager
from constants import screen_width, screen_height


class AnimationManager:
    def __init__(self):
        self.ongoingAnimations = []

    def uranium_pellet_animations(self,num_pellets:int=100):
        self.ongoingAnimations.append(UraniumPelletAnimation(num_pellets))

    def confetti_animations(self,source:tuple[int,int]):
        self.ongoingAnimations.append(ConfettiAnimation(source))

    def render(self, win: pygame.Surface):
        for animation in self.ongoingAnimations:
            result = animation.render(win)
            if result != 0:
                self.ongoingAnimations.remove(animation)

class ConfettiAnimation:
    def __init__(self,source:tuple[int,int]):
        self.source = source
        confetticolors = ['green','red','yellow','blue']
        self.confetti = [Confetti((self.source),random.choice(confetticolors)) for _ in range(100)]
    def render(self,win: pygame.Surface):

        for confetti in self.confetti:
            confetti.render(win)
            confetti.next_frame()
            if confetti.current_frame > 40:
                self.confetti.remove(confetti)
                del confetti
                return 1
        return 0

class Confetti:
    def __init__(self, position: tuple[int, int], color:str):
        self.start_position = position
        self.position = position
        self.color = color
        self.current_frame = 0
        self.drag = 0.0001
        self.g = -15
        self.timestep = 1/60
        directionAngle = random.randint(0, 360)

        direction = math.cos(directionAngle),math.sin(directionAngle)
        initialVelocity = random.randint(10,50)

        self.velocity = self.vec_scalar_mul(direction,initialVelocity, )

    def vector_add(self,vec1:tuple[float,float],vec2:tuple[float,float]):
        return (vec1[0]+vec2[0],vec1[1]+vec2[1])

    def vec_scalar_mul(self,vec:tuple[float,float],mul:float):
        return (vec[0]*mul,vec[1]*mul)

    def vector_magnitude(self,vec:tuple[float,float]):
        return math.sqrt(vec[0]**2+vec[1]**2)

    def next_frame(self):
        self.velocity = self.vector_add(
            self.velocity,
            self.vec_scalar_mul(self.velocity,-self.drag * self.vector_magnitude(self.velocity)**2 )
        )

        self.velocity = self.vector_add(self.velocity,(0,-self.g*self.timestep))

        self.position = self.vector_add(self.position,self.velocity)

        self.current_frame += 1

    def render(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, pygame.Rect(self.position, (10, 10)))


class UraniumPelletAnimation:
    def __init__(self,num_pellets:int):
        self.destination_rect = pygame.Rect((0, 0), (80, 20))
        self.destination_rect.center = (screen_width // 2, screen_height // 2)
        gameManager.money_desync = True
        self.pellets = [UraniumPellet((screen_width // 2, 100), 10, (screen_width // 2, screen_height // 2))
                        for _ in range(num_pellets)]

    def render(self, win: pygame.Surface):

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
            return 1
        return 0


class UraniumPellet:
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
