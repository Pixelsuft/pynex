import pygame
from . import *


class NImage:
    def __init__(
            self,
            parent: any,
            image: pygame.Surface,
            xy: tuple,
            auto_size: bool = True,
            stretch: bool = False
    ) -> None:
        super(NImage, self).__init__()
        self.image = image
        self.x, self.y = xy
        self.w, self.h = 0, 0
        self._width, self._height = self.w, self.h
        self.hook_mouse = True
        self.stretch = stretch
        self.auto_size = auto_size
        self.is_visible = True
        self.is_enabled = True
        self.is_focusable = True
        self.enable_scroll = True
        self.usable = True
        self.surface = self.image
        self.cursor = cursors.get('DEFAULT')
        self.z_order = 0
        self.tag = ''
        self.id = ''
        self.redraw()
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name in ('stretch', 'image', 'w', 'h'):
            self.redraw()
        return self

    def redraw(self) -> None:
        if self.stretch:
            self._width, self._height = self.w, self.h
            self.surface = pygame.transform.scale(self.image, (self.w, self.h))
        else:
            self.surface = self.image
            self._width, self._height = self.surface.get_size()
            if self.auto_size:
                self.w, self.h = self._width, self._height

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        surface.blit(
            self.surface,
            (self.x + scroll_x, self.y + scroll_y),
            None if self.auto_size else (0, 0, self.w, self.h)
        )

    def _on_mouse_wheel(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_wheel(  # type: ignore
                (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
            )

    def _on_mouse_leave(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_leave(event.pos)  # type: ignore

    def _on_mouse_enter(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_enter(event.pos)  # type: ignore

    def _on_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_move(  # type: ignore
                event.pos, event.rel, event.buttons, hasattr(event, 'touch') and event.touch
            )

    def _on_mouse_down(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_down(event.pos, event.button)  # type: ignore

    def _on_mouse_up(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_mouse_up(event.pos, event.button)  # type: ignore
        if event.button == pygame.BUTTON_LEFT and hasattr(self, 'on_click'):
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
