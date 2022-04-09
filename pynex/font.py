import pygame
from . import *


class NFont:
    def __init__(
            self,
            fn: str
    ) -> None:
        super(NFont, self).__init__()
        self.fn = fn

    def require_size(
            self,
            size: int
    ) -> pygame.font.Font:
        attr = f'font_{size}'
        if not hasattr(self, attr):
            setattr(self, attr, pygame.font.Font(self.fn, size))
        return getattr(self, attr)


class NChildFont:
    def __init__(
            self,
            parent: NFont,
            size: int
    ) -> None:
        super(NChildFont, self).__init__()
        self.parent = parent
        self.original_size = self.size = size
        self.font = self.parent.require_size(self.size)

    def scale(self, new_scale: float) -> None:
        self.size = round(self.original_size * new_scale)
        self.font = self.parent.require_size(self.size)
