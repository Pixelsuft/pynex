import pygame
from . import *


class NCheckBox:
    def __init__(
            self,
            parent: any,
            font: NFont,
            font_size: int,
            xy: tuple,
            text: str,
            color: tuple = (0, 0, 0),
            auto_size: bool = True,
            auto_size_box: bool = False,
            anti_alias: bool = True,
            stretch: bool = False
    ) -> None:
        super(NCheckBox, self).__init__()
        self.font_size = font_size
        self.font: NChildFont = font.create_size(self.font_size)
        self.x, self.y = xy
        self.w, self.h = 0, 0
        self._width, self._height = self.w, self.h
        self.anti_alias = anti_alias
        self.auto_size = auto_size
        self.auto_size_box = auto_size_box
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
        self.color1 = (255, 255, 255)
        self.color2 = (51, 51, 51)
        self.color3 = self.color2
        self.color1_hover = (255, 255, 255)
        self.color2_hover = (0, 120, 215)
        self.color3_hover = self.color2_hover
        self.color1_focus = (204, 228, 247)
        self.color2_focus = (0, 84, 153)
        self.color3_focus = self.color2_focus
        self.current_color1 = self.color1
        self.current_color2 = self.color2
        self.current_color3 = self.color3
        self.border_radius = 0
        self.padding = 3
        self.box_size = 13
        self.margin = 5
        self.checked = False
        self.auto_scale = True
        self.min_scale = 1.0
        self.scale_x, self.scale_y = 1.0, 1.0
        self.multi_lines_align = LABEL_ALIGN_LEFT
        self.surface: pygame.Surface = None  # type: ignore
        self.cursor = cursors.get('DEFAULT')
        self.color = color
        self.z_order = 0
        self.tag = ''
        self.id = ''
        self.set('text', text)
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name in ('text', 'color', 'anti_alias', 'mutli_line_align', 'stretch', 'auto_size'):
            self.redraw()
        elif name in ('font', 'font_size'):
            self.font = self.font.create_size(self.font_size)
            self.redraw()
        elif name in ('scale_x', 'scale_y'):
            self.min_scale = min(self.scale_x, self.scale_y)
            self.font.scale(self.min_scale)
            self.redraw()
        return self

    def redraw(self) -> None:
        if self.text.count('\n') <= 0:
            self.surface = self.font.font.render(
                self.text,
                self.anti_alias,
                self.color
            )
            self._width, self._height = self.surface.get_size()
            if self.auto_size:
                self.w, self.h = r(self._width / self.min_scale), r(self._height / self.min_scale)
            elif self.stretch:
                self.surface = pygame.transform.scale(
                    self.surface, round_tuple((self.w * self.scale_x, self.h * self.scale_y))
                )
            if self.auto_size_box:
                self.box_size = self.h
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
            self.w, self.h = r(self._width / self.min_scale), r(self._height / self.min_scale)
        elif self.stretch:
            self.surface = pygame.transform.scale(
                self.surface, round_tuple((self.w * self.scale_x, self.h * self.scale_y))
            )
        if self.auto_size_box:
            self.box_size = self.h

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        pygame.draw.rect(
            surface,
            self.current_color1,
            round_tuple((self.x * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
                         self.box_size * self.scale_x, self.box_size * self.scale_y)),
            0,
            r(self.border_radius * self.min_scale)
        )
        if self.checked:
            pygame.draw.rect(
                surface,
                self.current_color3,
                round_tuple((
                    (self.x + self.padding) * self.scale_x + scroll_x,
                    (self.y + self.padding) * self.scale_y + scroll_y,
                    (self.box_size - self.padding * 2) * self.scale_x,
                    (self.box_size - self.padding * 2) * self.scale_y
                )),
                0,
                r(self.border_radius * self.min_scale)
            )
        pygame.draw.rect(
            surface,
            self.current_color2,
            round_tuple((self.x * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
                         self.box_size * self.scale_x, self.box_size * self.scale_y)),
            r(self.min_scale) or 1,
            r(self.border_radius * self.min_scale)
        )
        surface.blit(
            self.surface,
            round_tuple(((self.box_size + self.margin + self.x + self.x_offset) * self.scale_x + scroll_x,
                         (self.y + self.y_offset) * self.scale_y + scroll_y)),
            None if self.auto_size else (0, 0, r((self.w - 1) * self.scale_x), r(self.h * self.scale_y))
        )

    def _on_mouse_wheel(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_wheel(  # type: ignore
                (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
            )

    def _on_mouse_leave(self, event: pygame.event.Event, bind: bool) -> None:
        self.current_color1 = self.color1
        self.current_color2 = self.color2
        self.current_color3 = self.color3
        if bind:
            self.on_mouse_leave(event.pos)  # type: ignore

    def _on_mouse_enter(self, event: pygame.event.Event, bind: bool) -> None:
        self.current_color1 = self.color1_hover
        self.current_color2 = self.color2_hover
        self.current_color3 = self.color3_hover
        if bind:
            self.on_mouse_enter(event.pos)  # type: ignore

    def _on_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_move(  # type: ignore
                event.pos, event.rel, event.buttons, hasattr(event, 'touch') and event.touch
            )

    def _on_mouse_down(self, event: pygame.event.Event, bind: bool) -> None:
        if event.button == pygame.BUTTON_LEFT:
            self.current_color1 = self.color1_focus
            self.current_color2 = self.color2_focus
            self.current_color3 = self.color3_focus
        if bind:
            self.on_mouse_down(event.pos, event.button)  # type: ignore

    def _on_mouse_up(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_up(event.pos, event.button)  # type: ignore
        if event.button == pygame.BUTTON_LEFT:
            self.current_color1 = self.color1_hover
            self.current_color2 = self.color2_hover
            self.current_color3 = self.color3_hover
            if self.checked:
                self.checked = False
            else:
                self.checked = True
            if hasattr(self, 'on_check'):
                self.on_check(self.checked)
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

    def __bool__(self) -> bool:
        return self.checked
