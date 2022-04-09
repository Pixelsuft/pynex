from . import *


class NProgressBar:
    def __init__(
            self,
            parent: any,
            xy: tuple,
            size: tuple = (120, 22),
            value: any = 0,
            min_value: any = 0,
            max_value: any = 100
    ) -> None:
        super(NProgressBar, self).__init__()
        self.x, self.y = xy
        self.w, self.h = size
        self.hook_mouse = True
        self.is_visible = True
        self.is_enabled = True
        self.is_focusable = True
        self.enable_scroll = True
        self.usable = True
        self.auto_scale = True
        self.scale_x, self.scale_y = 1.0, 1.0
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.cursor = cursors.get('DEFAULT')
        self.z_order = 0
        self.border_radius = 1
        self.border_color = (188, 188, 188)
        self.filled_color = (6, 176, 37)
        self.empty_color = (230, 230, 230)
        self.tag = ''
        self.id = ''
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        pygame.draw.rect(
            surface,
            self.empty_color,
            round_tuple((self.x * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
                         self.w * self.scale_x, self.h * self.scale_y))
        )
        pygame.draw.rect(
            surface,
            self.filled_color,
            (self.x * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
             ((self.value - self.min_value) / (self.max_value - self.min_value) * (self.w - self.border_radius * 2) +
              self.border_radius) * self.scale_x, self.h * self.scale_y)
        )
        pygame.draw.rect(
            surface,
            self.border_color,
            round_tuple((self.x * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
                         self.w * self.scale_x, self.h * self.scale_y)),
            self.border_radius
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
        if event.button == pygame.BUTTON_LEFT:
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
