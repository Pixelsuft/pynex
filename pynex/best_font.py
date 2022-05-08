import pygame
from . import *


class NFont:
    def __init__(
            self,
            fn: str
    ) -> None:
        super(NFont, self).__init__()
        self.fn = fn
        self.font_cache_scale = 1.0

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def require_size(
            self,
            size: int
    ) -> pygame.font.Font:
        sz = round(size * self.font_cache_scale)
        attr = f'font_{sz}'
        if not hasattr(self, attr):
            setattr(self, attr, pygame.font.Font(self.fn, sz))
        return getattr(self, attr)

    def create_size(self, size: int) -> any:
        return NChildFont(self, size)


class NChildFont:
    def __init__(
            self,
            parent: NFont,
            size: int
    ) -> None:
        super(NChildFont, self).__init__()
        self.parent = parent
        self.original_size = self.size = size
        self.original_font = self.font = self.parent.require_size(self.size)
        self.scale_x = self.scale_y = self.avg_scale = 1.0
        self.line_height = self.font.get_linesize()

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def create_size(self, size: int) -> any:
        return self.parent.create_size(size)

    def scale(self, scale_x: float, scale_y: float, avg_scale: float) -> None:
        self.scale_x, self.scale_y = scale_x, scale_y
        self.avg_scale = avg_scale
        self.size = round(self.original_size * self.avg_scale)
        self.font = self.parent.require_size(self.size)
        self.line_height = self.font.get_linesize()

    def render(self, text: any, anti_alias: bool, color, background: any = None) -> pygame.Surface:
        orig_size = self.original_font.size(text)
        return pygame.transform.scale(
            self.font.render(text, anti_alias, color, background),
            (orig_size[0] * self.scale_x, orig_size[1] * self.scale_y)
        )
