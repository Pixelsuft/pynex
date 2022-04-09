import pygame
from . import *


class NWinAnimatedButton:
    def __init__(
            self,
            parent: any,
            font: NFont,
            font_size: int,
            xy: tuple,
            text: str,
            size: tuple,
            color: tuple = (0, 0, 0),
            animation_time: any = 0.2,
            anti_alias: bool = True,
            auto_size: bool = False,
            stretch: bool = False
    ) -> None:
        super(NWinAnimatedButton, self).__init__()
        self.font_size = font_size
        self.font: NChildFont = font.create_size(self.font_size)
        self.x, self.y = xy
        self.w, self.h = size
        self._width, self._height = self.w, self.h
        self.anti_alias = anti_alias
        self.auto_size = auto_size
        self.stretch = stretch
        self.hook_mouse = True
        self.is_visible = True
        self.is_enabled = True
        self.is_focusable = True
        self.enable_scroll = True
        self.usable = True
        self.text = text
        self.x_offset = 0
        self.y_offset = 0
        self.multi_lines_align = LABEL_ALIGN_LEFT
        self.surface: pygame.Surface = None  # type: ignore
        self.cursor = cursors.get('DEFAULT')
        self.color = color
        self.color1 = (225, 225, 225)
        self.color2 = (173, 173, 173)
        self.hover_color1 = (229, 241, 251)
        self.hover_color2 = (0, 120, 215)
        self.focus_color1 = (204, 228, 247)
        self.focus_color2 = (0, 84, 153)
        self.animation_time = animation_time
        self.current_color1 = NSimpleColorFade(None, self.color1, self.color1, self.animation_time, False)
        self.current_color2 = NSimpleColorFade(None, self.color2, self.color2, self.animation_time, False)
        self.border_radius = 0
        self.x_align = WIN_BUTTON_ALIGN_CENTER
        self.y_align = WIN_BUTTON_ALIGN_CENTER
        self.auto_size_margin_x = 5
        self.auto_size_margin_y = 5
        self.align_x_offset = 0
        self.align_y_offset = 0
        self.auto_scale = True
        self.min_scale = 1.0
        self.scale_x, self.scale_y = 1.0, 1.0
        self.z_order = 0
        self.tag = ''
        self.id = ''
        self.set('text', text)
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name in (
                'text', 'color', 'anti_alias', 'mutli_line_align', 'stretch', 'auto_size',
                'auto_size_margin_x', 'auto_size_margin_y'
        ):
            self.redraw()
            self.calc_align()
        elif name in ('x_align', 'y_align'):
            self.calc_align()
        elif name in ('font', 'font_size'):
            self.font = self.font.create_size(self.font_size)
            self.redraw()
        elif name in ('scale_x', 'scale_y'):
            self.min_scale = min(self.scale_x, self.scale_y)
            self.font.scale(self.min_scale)
            self.redraw()
        return self

    def calc_align(self) -> None:
        if self.auto_size or self.stretch:
            self.align_x_offset = self.auto_size_margin_x
            self.align_y_offset = self.auto_size_margin_y
            return
        if self.x_align == WIN_BUTTON_ALIGN_LEFT:
            self.align_x_offset = 0
        elif self.x_align == WIN_BUTTON_ALIGN_CENTER:
            self.align_x_offset = round((self.w - 2) / 2 - self.surface.get_width() / 2)
        elif self.x_align == WIN_BUTTON_ALIGN_RIGHT:
            self.align_x_offset = self.w - self.surface.get_width()
        if self.y_align == WIN_BUTTON_ALIGN_TOP:
            self.align_y_offset = 0
        elif self.y_align == WIN_BUTTON_ALIGN_CENTER:
            self.align_y_offset = round((self.h - 2) / 2 - self.surface.get_height() / 2)
        elif self.y_align == WIN_BUTTON_ALIGN_BOTTOM:
            self.align_y_offset = self.h - self.surface.get_height()

    def redraw(self) -> None:
        if self.text.count('\n') <= 0:
            self.surface = self.font.font.render(
                self.text,
                self.anti_alias,
                self.color
            )
            self._width, self._height = self.surface.get_size()
            if self.auto_size:
                self.w, self.h =\
                    r((self._width + self.auto_size_margin_x * 2 + 1) / self.min_scale),\
                    r((self._height + self.auto_size_margin_y * 2 + 1) / self.min_scale)
            elif self.stretch:
                self.surface = pygame.transform.scale(
                    self.surface, round_tuple((self.w * self.scale_x, self.h * self.scale_y))
                )
            return
        total_height = 0
        max_width = 0
        surfaces = []
        heights = []
        for _text in self.text.split('\n'):
            _surface = self.font.font.render(
                _text,
                self.anti_alias,
                self.color
            )
            total_height += _surface.get_height()
            max_width = max(max_width, _surface.get_width())
            surfaces.append(_surface)
            heights.append(_surface.get_height())
        self._width, self._height = max_width, total_height
        self.surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA, 32)
        total_height = 0
        for _num, _surface in enumerate(surfaces):
            self.surface.blit(
                _surface, (
                    0 if self.multi_lines_align == LABEL_ALIGN_LEFT else (
                        max_width - _surface.get_width() if self.multi_lines_align == LABEL_ALIGN_RIGHT else
                        round(max_width / 2 - _surface.get_width() / 2)
                    ),
                    total_height
                )
            )
            total_height += heights[_num]
        if self.auto_size:
            self.w, self.h =\
                r((self._width + self.auto_size_margin_x * 2 + 1) / self.min_scale),\
                r((self._height + self.auto_size_margin_y * 2 + 1) / self.min_scale)
        elif self.stretch:
            self.surface = pygame.transform.scale(
                self.surface, round_tuple((self.w * self.scale_x, self.h * self.scale_y))
            )

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        self.current_color1.draw(surface, delta, scroll_x, scroll_y)
        self.current_color2.draw(surface, delta, scroll_x, scroll_y)
        pygame.draw.rect(
            surface,
            self.current_color1.color,
            round_tuple(((self.x + self.x_offset) * self.scale_x + scroll_x,
                         (self.y + self.y_offset) * self.scale_y + scroll_y,
                         self.w * self.scale_x, self.h * self.scale_y)),
            0,
            self.border_radius
        )
        pygame.draw.rect(
            surface,
            self.current_color2.color,
            round_tuple(((self.x + self.x_offset) * self.scale_x + scroll_x,
                         (self.y + self.y_offset) * self.scale_y + scroll_y,
                         self.w * self.scale_x, self.h * self.scale_y)),
            r(self.min_scale) or 1,
            self.border_radius
        )
        surface.blit(
            self.surface,
            (
                r((self.x + self.x_offset + 1) * self.scale_x + scroll_x),
                r((self.y + self.y_offset + 1) * self.scale_y + scroll_y)
            ),
            round_tuple((-self.align_x_offset * self.scale_x, -self.align_y_offset * self.scale_y,
                         (self.w - 2) * self.scale_x, (self.h - 2) * self.scale_y))
        )

    def _on_mouse_wheel(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_wheel(  # type: ignore
                (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
            )

    def _on_mouse_leave(self, event: pygame.event.Event, bind: bool) -> None:
        self.current_color1.create(self.current_color1.color, self.color1, self.animation_time)
        self.current_color2.create(self.current_color2.color, self.color2, self.animation_time)
        if bind:
            self.on_mouse_leave(event.pos)  # type: ignore

    def _on_mouse_enter(self, event: pygame.event.Event, bind: bool) -> None:
        self.current_color1.create(self.current_color1.color, self.hover_color1, self.animation_time)
        self.current_color2.create(self.current_color2.color, self.hover_color2, self.animation_time)
        if bind:
            self.on_mouse_enter(event.pos)  # type: ignore

    def _on_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_move(  # type: ignore
                event.pos, event.rel, event.buttons, hasattr(event, 'touch') and event.touch
            )

    def _on_mouse_down(self, event: pygame.event.Event, bind: bool) -> None:
        if event.button == pygame.BUTTON_LEFT:
            self.current_color1.create(self.current_color1.color, self.focus_color1, self.animation_time)
            self.current_color2.create(self.current_color2.color, self.focus_color2, self.animation_time)
        if bind:
            self.on_mouse_down(event.pos, event.button)  # type: ignore

    def _on_mouse_up(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_up(event.pos, event.button)  # type: ignore
        if event.button == pygame.BUTTON_LEFT:
            self.current_color1.create(self.current_color1.color, self.hover_color1, self.animation_time)
            self.current_color2.create(self.current_color2.color, self.hover_color2, self.animation_time)
            if hasattr(self, 'on_click'):
                self.on_click(event.pos)

    def _on_focus_enter(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_focus_enter(event.pos, event.button)  # type: ignore

    def _on_focus_leave(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_focus_leave(event.pos, event.button)  # type: ignore

    def _on_key_down(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_key_down(event)  # type: ignore

    def _on_key_up(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_key_up(event)  # type: ignore
