import pygame
from . import *


class NFrame:
    def __init__(
            self,
            parent: any,
            xy: tuple,
            size: tuple
    ) -> None:
        super(NFrame, self).__init__()
        self.x, self.y = xy
        self.w, self.h = size
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.hook_mouse = True
        self.is_visible = True
        self.is_enabled = True
        self.is_focusable = True
        self.enable_scroll = True
        self.is_mouse_left_down = False
        self.is_mouse_enter = False
        self.usable = True
        self.auto_scale = True
        self.scale_x = self.scale_y = self.min_scale = self.max_scale = self.avg_scale = 1.0
        self.scroll_x, self.scroll_y = 0, 0
        self._scroll_x, self._scroll_y = 0, 0
        self.cursor = cursors.get('DEFAULT')
        self.current_cursor = self.cursor
        self.last_hover = self
        self.last_focus = self
        self.child = NChildCollector()
        self.find_by_tag = self.child.find_by_tag
        self.find_by_id = self.child.find_by_id
        self.add_child = self.child.add_child
        self.remove_child = self.child.remove_child
        self.export_child = self.child.export_child
        self.import_child = self.child.import_child
        self.sort_child = self.child.sort
        self.last_cursor_pos = (0, 0)
        self.z_order = 0
        self.tag = ''
        self.id = ''
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name in ('w', 'h'):
            self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        elif name == 'scale_x':
            for child in self.child.child:
                if child.usable and child.auto_scale:
                    child.set('min_scale', min(self.scale_x, child.scale_y))
                    child.set('max_scale', max(self.scale_x, child.scale_y))
                    child.set('avg_scale', (self.scale_x + child.scale_y) / 2)
                    child.set('scale_x', self.scale_x)
        elif name == 'scale_y':
            for child in self.child.child:
                if child.usable and child.auto_scale:
                    child.set('min_scale', min(child.scale_x, self.scale_y))
                    child.set('max_scale', max(child.scale_x, self.scale_y))
                    child.set('avg_scale', (child.scale_x + self.scale_y) / 2)
                    child.set('scale_y', self.scale_y)
        return self

    def is_self_hover(self) -> bool:
        return self.last_hover == self

    def is_self_focus(self) -> bool:
        return self.last_focus == self

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        self.on_before_draw()
        for child in self.child.child:
            child.draw(self.surface, delta, self.scroll_x, self.scroll_y)
        self.on_after_draw()
        surface.blit(
            self.surface,
            (r(self.x * self.scale_x) + scroll_x, r(self.y * self.scale_y) + scroll_y)
        )

    def on_before_draw(self) -> None:
        self.surface.fill((0, 0, 0, 0))

    def on_after_draw(self) -> None:
        pass

    def on_mouse_process(self, xy: tuple) -> tuple:
        x, y = xy
        if self.enable_scroll:
            x -= self._scroll_x
            y -= self._scroll_y
        x -= self.x * self.scale_x
        y -= self.y * self.scale_y
        return r(x), r(y)

    def _on_mouse_wheel(self, event: pygame.event.Event, bind: bool) -> None:
        if hasattr(self.last_focus, '_on_mouse_wheel'):
            if not self.is_self_focus():
                self.last_focus._on_mouse_wheel(event, hasattr(self.last_focus, 'on_mouse_wheel'))
            elif bind:
                self.on_mouse_wheel(  # type: ignore
                    (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
                )
        if hasattr(self, 'on_global_mouse_wheel'):
            self.on_global_mouse_wheel(
                (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
            )

    def _on_mouse_leave(self, event: pygame.event.Event, bind: bool) -> None:
        self.is_mouse_enter = False
        event.pos = self.on_mouse_process(event.pos)
        if not self.is_mouse_left_down and not self.is_self_hover():
            self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
            self.last_hover = self
            if bind:
                self.on_mouse_leave(event.pos)  # type: ignore
        if hasattr(self, 'on_global_mouse_leave'):
            self.on_global_mouse_leave(event)

    def _on_mouse_enter(self, event: pygame.event.Event, bind: bool) -> None:
        self.is_mouse_enter = True
        event.pos = self.on_mouse_process(event.pos)
        self.last_cursor_pos = event.pos
        if hasattr(self, 'on_global_mouse_enter'):
            self.on_global_mouse_enter(event.pos)

    def _on_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
        event.pos = self.on_mouse_process(event.pos)
        self.last_cursor_pos = event.pos
        if not self.is_mouse_left_down:
            hover = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled and\
                        is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    hover = child
                    break
            if not hover == self.last_hover:
                if hasattr(self.last_hover, '_on_mouse_leave'):
                    if self.is_self_hover():
                        if hasattr(self, 'on_mouse_leave'):
                            self.on_mouse_leave(event.pos)
                    else:
                        self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = hover
                if not self.last_hover.cursor == self.current_cursor:
                    pygame.mouse.set_cursor(self.last_hover.cursor)
                    self.current_cursor = self.last_hover.cursor
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_enter'):
                        self.on_mouse_enter(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
        if self.is_self_hover():
            if hasattr(self, 'on_mouse_move'):
                self.on_mouse_move(event.pos, event.rel, event.buttons, hasattr(event, 'touch') and event.touch)
        elif hasattr(self.last_hover, '_on_mouse_move'):
            self.last_hover._on_mouse_move(event, hasattr(self.last_hover, 'on_mouse_move'))
        if hasattr(self, 'on_global_mouse_move'):
            self.on_global_mouse_move(
                event.pos, event.rel, event.buttons, hasattr(event, 'touch') and event.touch
            )

    def _on_mouse_down(self, event: pygame.event.Event, bind: bool) -> None:
        event.pos = self.on_mouse_process(event.pos)
        if event.button == pygame.BUTTON_LEFT:
            self.is_mouse_left_down = True
            hover = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled\
                        and is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    hover = child
                    break
            if not hover == self.last_hover:
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_leave'):
                        self.on_mouse_leave(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = hover
                if not self.last_hover.cursor == self.current_cursor:
                    pygame.mouse.set_cursor(self.last_hover.cursor)
                    self.current_cursor = self.last_hover.cursor
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_enter'):
                        self.on_mouse_enter(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
            focus = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled and \
                        is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    focus = child
                    break
            if not focus == self.last_focus:
                if self.is_self_focus():
                    if hasattr(self, 'on_focus_leave'):
                        self.on_focus_leave(event.pos, event.button)
                elif hasattr(self.last_focus, '_on_focus_leave'):
                    self.last_focus._on_focus_leave(event, hasattr(self.last_focus, 'on_focus_leave'))
                self.last_focus = focus
                if self.is_self_focus():
                    if hasattr(self, 'on_focus_enter'):
                        self.on_focus_enter(event.pos, event.button)
                elif hasattr(self.last_focus, '_on_focus_enter'):
                    self.last_focus._on_focus_enter(event, hasattr(self.last_focus, 'on_focus_enter'))
        if self.is_self_hover():
            if hasattr(self, 'on_mouse_down'):
                self.on_mouse_down(event.pos, event.button)
        elif hasattr(self.last_hover, '_on_mouse_down'):
            self.last_hover._on_mouse_down(event, hasattr(self.last_hover, 'on_mouse_down'))
        if hasattr(self, 'on_global_mouse_down'):
            self.on_global_mouse_down(event.pos, event.button)

    def _on_mouse_up(self, _event: pygame.event.Event, bind: bool) -> None:
        event = pygame.event.Event(pygame.MOUSEBUTTONUP)
        event.button = _event.button
        event.pos = self.on_mouse_process(_event.pos)
        if event.button == pygame.BUTTON_LEFT:
            self.is_mouse_left_down = False
        if self.is_self_hover():
            if hasattr(self, 'on_mouse_up'):
                self.on_mouse_up(event.pos, event.button)
            if event.button == pygame.BUTTON_LEFT and hasattr(self, 'on_click'):
                self.on_click(event.pos)
        elif hasattr(self.last_hover, '_on_mouse_up'):
            self.last_hover._on_mouse_up(event, hasattr(self.last_hover, 'on_mouse_up'))
        if event.button == pygame.BUTTON_LEFT:
            hover = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled and\
                        is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    hover = child
                    break
            if not hover == self.last_hover:
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_leave'):
                        self.on_mouse_leave(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = hover
                if not self.last_hover.cursor == self.current_cursor:
                    pygame.mouse.set_cursor(self.last_hover.cursor)
                    self.current_cursor = self.last_hover.cursor
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_enter'):
                        self.on_mouse_enter(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
            elif is_android:
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_leave'):
                        self.on_mouse_leave(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = self
                if self.is_self_hover():
                    if hasattr(self, 'on_mouse_enter'):
                        self.on_mouse_enter(event.pos)
                elif hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
            if hasattr(self, 'on_global_click'):
                self.on_global_click(event.pos)
        if hasattr(self, 'on_global_mouse_up'):
            self.on_global_mouse_up(event.pos, event.button)

    def _on_focus_enter(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_focus_enter(event.pos, event.button)  # type: ignore

    def _on_focus_leave(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_focus_leave(event.pos, event.button)  # type: ignore

    def _on_key_down(self, event: pygame.event.Event, bind: bool) -> None:
        if self.is_self_focus():
            if hasattr(self, 'on_key_down'):
                self.on_key_down(event)
        elif hasattr(self.last_focus, '_on_key_down'):
            self.last_focus._on_key_down(event, hasattr(self.last_focus, 'on_key_down'))
        if hasattr(self, 'on_global_keydown'):
            self.on_global_keydown(event)

    def _on_key_up(self, event: pygame.event.Event, bind: bool) -> None:
        if self.is_self_focus():
            if hasattr(self, 'on_key_up'):
                self.on_key_up(event)
        elif hasattr(self.last_focus, '_on_key_up'):
            self.last_focus._on_key_up(event, hasattr(self.last_focus, 'on_key_up'))
        if hasattr(self, 'on_global_keyup'):
            self.on_global_keyup(event)
