import pygame
from . import *


class NSimpleColorFade:
    def __init__(
            self,
            parent: any,
            from_color: tuple = (0, 0, 0),
            to_color: tuple = (255, 255, 255),
            time: any = 1,
            auto_start: bool = True
    ) -> None:
        super(NSimpleColorFade, self).__init__()
        self.from_color = from_color
        self.to_color = to_color
        self.time = float(time)
        self.speed = (0.0, 0.0, 0.0)
        self.current_color = [
            float(self.to_color[0]),
            float(self.to_color[1]),
            float(self.to_color[2])
        ]
        self.color = round_tuple(self.current_color)
        self.current_rate = 0.0
        self.usable = False
        self.is_enabled = False
        if auto_start:
            self.create(from_color, to_color, time)
        if parent:
            parent.add_child(self)

    def create(self, from_color: tuple, to_color: tuple, time: any, should_enable: bool = True) -> None:
        self.from_color = from_color
        self.to_color = to_color
        self.time = float(time)
        self.speed = (
            (self.to_color[0] - self.from_color[0]) / self.time,
            (self.to_color[1] - self.from_color[1]) / self.time,
            (self.to_color[2] - self.from_color[2]) / self.time
        )
        self.current_color[0] = float(self.from_color[0])
        self.current_color[1] = float(self.from_color[1])
        self.current_color[2] = float(self.from_color[2])
        self.color = round_tuple(self.color)
        self.current_rate = 0.0
        if should_enable:
            self.is_enabled = True

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_enabled:
            return
        self.current_color[0] += self.speed[0] * delta
        self.current_color[1] += self.speed[1] * delta
        self.current_color[2] += self.speed[2] * delta
        self.current_rate += delta
        if self.current_rate >= self.time:
            self.is_enabled = False
            self.current_rate = 0.0
            self.current_color[0] = float(self.to_color[0])
            self.current_color[1] = float(self.to_color[1])
            self.current_color[2] = float(self.to_color[2])
        self.color = round_tuple(self.current_color)
