import pygame
from . import *


class NVerticalSlider:
    def __init__(
            self,
            parent: any,
            xy: tuple,
            size: tuple = (22, 160),
            value: any = 0,
            min_value: any = 0,
            max_value: any = 99
    ) -> None:
        super(NVerticalSlider, self).__init__()
        self.x, self.y = xy
        self.w, self.h = size
        self.hook_mouse = True
        self.is_visible = True
        self.is_enabled = True
        self.is_focusable = True
        self.enable_scroll = True
        self.usable = True
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.single_step = 1
        self.page_step = 10
        self.slider_height = 10
        self.bar_hovered = False
        self.bar_focused = False
        self.down_it = False
        self.auto_scale = True
        self.min_scale = 1.0
        self.scale_x, self.scale_y = 1.0, 1.0
        self.bar_width = 4
        self.bar_top = 0
        self.lsx, self.lsy = 0, 0
        self.last_y_focus = 0
        self.bar_border_color = (214, 214, 214)
        self.bar_color = (231, 234, 234)
        self.color = (0, 120, 215)
        self.hover_color = (23, 23, 23)
        self.focus_color = (204, 204, 204)
        self.current_color = self.color
        self.cursor = cursors.get('DEFAULT')
        self.z_order = 0
        self.tag = ''
        self.id = ''
        self.recalc_pos()
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name in ('bar_width', ):
            self.recalc_pos()
        elif name in ('scale_x', 'scale_y'):
            self.min_scale = min(self.scale_x, self.scale_y)
        return self

    def recalc_pos(self) -> None:
        self.bar_top = round(self.w / 2 - self.bar_width / 2)

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        self.lsx, self.lsy = scroll_x, scroll_y
        pygame.draw.rect(
            surface,
            self.bar_color,
            round_tuple(((self.x + self.bar_top + 1) * self.scale_x + scroll_x, (self.y + 1) * self.scale_y + scroll_y,
                         (self.bar_width - 1) * self.scale_x, (self.h - 1) * self.scale_y))
        )
        pygame.draw.rect(
            surface,
            self.bar_border_color,
            round_tuple(((self.x + self.bar_top) * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
                         self.bar_width * self.scale_x, self.h * self.scale_y)),
            r(self.min_scale) or 1
        )
        pygame.draw.rect(
            surface,
            self.current_color,
            round_tuple((self.x * self.scale_x + scroll_x, (self.y + (self.h - self.slider_height -
                                                                      (self.value - self.min_value) /
                                                                      (self.max_value - self.min_value) *
                                                                      (self.h - self.slider_height))) *
                         self.scale_y + scroll_y, self.w * self.scale_x, self.slider_height * self.scale_y))
        )

    def _on_mouse_wheel(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_wheel(  # type: ignore
                (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
            )

    def _on_mouse_leave(self, event: pygame.event.Event, bind: bool) -> None:
        if not self.bar_focused:
            self.bar_hovered = False
            self.current_color = self.color
        if bind:
            self.on_mouse_leave(event.pos)  # type: ignore

    def _on_mouse_enter(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_enter(event.pos)  # type: ignore

    def _on_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
        if self.bar_focused:
            y = event.pos[1] - self.y * self.scale_y - self.lsy - self.last_y_focus
            value = (self.h - self.slider_height - y) / self.scale_y / (self.h - self.slider_height) *\
                    (self.max_value - self.min_value) + self.min_value
            if value < self.min_value:
                value = self.min_value
            elif value > self.max_value:
                value = self.max_value
            self.value = value
            if hasattr(self, 'on_change'):
                self.on_change(value)
        elif not self.down_it:
            if is_colliding_rect(
                    (self.x * self.scale_x + self.lsx,
                     (self.y + (self.h - self.slider_height - (self.value - self.min_value) /
                                (self.max_value - self.min_value) * (self.h - self.slider_height))) *
                     self.scale_y + self.lsy, self.w * self.scale_x, self.slider_height * self.scale_y), event.pos
            ):
                if not self.bar_hovered:
                    self.bar_hovered = True
                    self.current_color = self.hover_color
            elif self.bar_hovered:
                self.bar_hovered = False
                self.current_color = self.color
        if bind:
            self.on_mouse_move(  # type: ignore
                event.pos, event.rel, event.buttons, hasattr(event, 'touch') and event.touch
            )

    def _on_mouse_down(self, event: pygame.event.Event, bind: bool) -> None:
        if event.button == pygame.BUTTON_LEFT:
            if self.bar_hovered:
                self.bar_focused = True
                self.current_color = self.focus_color
                self.last_y_focus = event.pos[1] - self.y * self.scale_y - self.lsy - self.h + self.slider_height +\
                    ((self.value - self.min_value) / (self.max_value - self.min_value) *
                     (self.h - self.slider_height) * self.scale_y)
            else:
                self.down_it = True
                if event.pos[1] > (
                        (self.y + self.h - self.slider_height - ((self.value - self.min_value) /
                                                                 (self.max_value - self.min_value) *
                                                                 (self.h - self.slider_height)) +
                         self.slider_height / 2) * self.scale_y + self.lsy
                ):
                    self.value -= self.page_step
                    if self.value < self.min_value:
                        self.value = self.min_value
                else:
                    self.value += self.page_step
                    if self.value > self.max_value:
                        self.value = self.max_value
                if hasattr(self, 'on_change'):
                    self.on_change(self.value)
        if bind:
            self.on_mouse_down(event.pos, event.button)  # type: ignore

    def _on_mouse_up(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_up(event.pos, event.button)  # type: ignore
        if event.button == pygame.BUTTON_LEFT:
            self.down_it = False
            if self.bar_focused:
                self.bar_focused = False
                self.current_color = self.hover_color
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
