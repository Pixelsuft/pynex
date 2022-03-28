import time
import pygame
from . import *


class NTimer:
    def __init__(
            self,
            parent: any,
            rate: any,
            repeat: bool = True,
            smooth_fix: bool = True,
            auto_start: bool = True,
            first_tick: bool = False
    ) -> None:
        super(NTimer, self).__init__()
        self.rate = float(rate)
        self.smooth_fix = smooth_fix
        self.repeat = repeat
        self.first_tick = first_tick
        self.usable = False
        self.is_enabled = False
        self.z_order = -999
        self.id = 0
        self.current_rate = 0.0
        if auto_start:
            self.run()
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def on_tick(self, delta: float) -> None:
        pass

    def run(self) -> None:
        self.is_enabled = True
        self.current_rate = self.rate if self.first_tick else 0.0

    def stop(self) -> None:
        self.is_enabled = False

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_enabled:
            return
        self.current_rate += delta
        while self.current_rate >= self.rate:
            if self.smooth_fix:
                self.current_rate -= self.rate
                self.on_tick(self.rate)
            else:
                self.on_tick(self.current_rate)
                self.current_rate = 0
            if not self.repeat:
                self.is_enabled = False
