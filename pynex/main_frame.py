import pygame
from . import *


class NMainFrame:
    def __init__(
            self,
            surface: pygame.Surface
    ) -> None:
        super(NMainFrame, self).__init__()
        self.surface = surface
        self.w, self.h = self.surface.get_size()
        self.processes = {
            pygame.QUIT: 'on_quit',
            pygame.WINDOWRESIZED: 'on_resize',
            pygame.KEYDOWN: 'on_global_key_down',
            pygame.KEYUP: 'on_global_key_up',
            pygame.MOUSEBUTTONDOWN: 'on_global_mouse_down',
            pygame.MOUSEBUTTONUP: 'on_global_mouse_up',
            pygame.MOUSEMOTION: 'on_global_mouse_move',
            pygame.MOUSEWHEEL: 'on_global_mouse_wheel'
        }
        self.hook_mouse = True
        self.is_focusable = True
        self.is_mouse_left_down = False
        self.scroll_x, self.scroll_y = 0, 0
        if not cursors:
            compile_cursors()
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

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def process_events(self, events: list) -> list:
        for event in events:
            func = self.processes.get(event.type)
            if not func:
                continue
            getattr(self, '_' + func)(event, hasattr(self, func))
        return events

    def draw(
            self,
            delta: float
    ) -> None:
        for child in self.child.child:
            child.draw(self.surface, delta, self.scroll_x, self.scroll_y)

    def _on_quit(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_quit()  # type: ignore

    def _on_resize(self, event: pygame.event.Event, bind: bool) -> None:
        self.w, self.h = event.x, event.y
        if bind:
            self.on_resize(event.x, event.y)  # type: ignore

    def _on_global_key_down(self, event: pygame.event.Event, bind: bool) -> None:
        if hasattr(self.last_focus, '_on_key_down'):
            self.last_focus._on_key_down(event, hasattr(self.last_focus, 'on_key_down'))
        if bind:
            self.on_global_key_down(event)  # type: ignore

    def _on_global_key_up(self, event: pygame.event.Event, bind: bool) -> None:
        if hasattr(self.last_focus, '_on_key_up'):
            self.last_focus._on_key_up(event, hasattr(self.last_focus, 'on_key_up'))
        if bind:
            self.on_global_key_up(event)  # type: ignore

    def _on_global_mouse_down(self, event: pygame.event.Event, bind: bool) -> None:
        if event.button == pygame.BUTTON_LEFT:
            self.is_mouse_left_down = True
            hover = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    hover = child
                    break
            if not hover == self.last_hover:
                if hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = hover
                if not self.last_hover.cursor == self.current_cursor:
                    pygame.mouse.set_cursor(self.last_hover.cursor)
                    self.current_cursor = self.last_hover.cursor
                if hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
            focus = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled and \
                        is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    focus = child
                    break
            if not focus == self.last_focus:
                if hasattr(self.last_focus, '_on_focus_leave'):
                    self.last_focus._on_focus_leave(event, hasattr(self.last_focus, 'on_focus_leave'))
                self.last_focus = focus
                if hasattr(self.last_focus, '_on_focus_enter'):
                    self.last_focus._on_focus_enter(event, hasattr(self.last_focus, 'on_focus_enter'))
        if hasattr(self.last_hover, '_on_mouse_down'):
            self.last_hover._on_mouse_down(event, hasattr(self.last_hover, 'on_mouse_down'))
        if bind:
            self.on_global_mouse_down(event.pos, event.button)  # type: ignore

    def _on_global_mouse_up(self, event: pygame.event.Event, bind: bool) -> None:
        if event.button == pygame.BUTTON_LEFT:
            self.is_mouse_left_down = False
        if hasattr(self.last_hover, '_on_mouse_up'):
            self.last_hover._on_mouse_up(event, hasattr(self.last_hover, 'on_mouse_up'))
        if event.button == pygame.BUTTON_LEFT:
            hover = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled and\
                        is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    hover = child
                    break
            if not hover == self.last_hover:
                if hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = hover
                if not self.last_hover.cursor == self.current_cursor:
                    pygame.mouse.set_cursor(self.last_hover.cursor)
                    self.current_cursor = self.last_hover.cursor
                if hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
            elif is_android:  # TODO: do something
                if hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = self
                if hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
        if bind:
            self.on_global_mouse_up(event.pos, event.button)  # type: ignore

    def _on_global_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
        if not self.is_mouse_left_down:
            hover = self
            for child in self.child.child[::-1]:
                if child.usable and child.hook_mouse and child.is_enabled and\
                        is_colliding(child, event.pos, self.scroll_x, self.scroll_y):
                    hover = child
                    break
            if not hover == self.last_hover:
                if hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = hover
                if not self.last_hover.cursor == self.current_cursor:
                    pygame.mouse.set_cursor(self.last_hover.cursor)
                    self.current_cursor = self.last_hover.cursor
                if hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
        if hasattr(self.last_hover, '_on_mouse_move'):
            self.last_hover._on_mouse_move(event, hasattr(self.last_hover, 'on_mouse_move'))
        if bind:
            self.on_global_mouse_move(event.pos)  # type: ignore

    def _on_global_mouse_wheel(self, event: pygame.event.Event, bind: bool) -> None:
        if hasattr(self.last_focus, '_on_mouse_wheel'):
            self.last_focus._on_mouse_wheel(event, hasattr(self.last_focus, 'on_mouse_wheel'))
        if bind:
            self.on_global_mouse_wheel(  # type: ignore
                (event.x, event.y), hasattr(event, 'touch') and event.touch, event.flipped
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
