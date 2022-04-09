import pygame
from . import *


class NFont:
    def __init__(
            self,
            fn: str
    ) -> None:
        super(NFont, self).__init__()
        self.fn = fn
        self.scale_slow_fix = False
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
        return (NFixedChildFont if self.font_cache_scale else NChildFont)(self, size)


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
        self.line_height = self.font.get_linesize()

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def create_size(self, size: int) -> any:
        return self.parent.create_size(size)

    def scale(self, new_scale: float) -> None:
        self.size = round(self.original_size * new_scale)
        self.font = self.parent.require_size(self.size)
        self.line_height = self.font.get_linesize()


class NFixedChildFont:
    def __init__(
            self,
            parent: NFont,
            size: int
    ) -> None:
        super(NFixedChildFont, self).__init__()
        self.parent = parent
        self.original_size = self.size = size
        self.font = self.parent.require_size(self.size)
        self.line_height = self.original_line_height = self.font.get_linesize()

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def create_size(self, size: int) -> any:
        return self.parent.create_size(size)

    def scale(self, new_scale: float) -> None:
        need_height = self.original_line_height * new_scale
        need_size = round(self.original_size * new_scale)
        font = self.parent.require_size(need_size)
        lh = font.get_linesize()
        if lh == need_height:
            self.line_height = lh
            return
        if lh > need_height:
            while lh > need_height and need_size > 0:
                need_size -= 1
                font = self.parent.require_size(need_size)
                lh = font.get_linesize()
        else:
            while lh < need_height:
                need_size += 1
                font = self.parent.require_size(need_size)
                lh = font.get_linesize()
        self.font = font
        self.line_height = lh
