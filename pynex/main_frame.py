import math

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
            0: 'on_unknown_event',
            pygame.AUDIODEVICEADDED: 'on_audio_device_added',
            pygame.AUDIODEVICEREMOVED: 'on_audio_device_removed',
            pygame.ACTIVEEVENT: 'on_active',
            pygame.KEYDOWN: 'on_global_key_down',
            pygame.KEYUP: 'on_global_key_up',
            pygame.MOUSEBUTTONDOWN: 'on_global_mouse_down',
            pygame.MOUSEBUTTONUP: 'on_global_mouse_up',
            pygame.MOUSEMOTION: 'on_global_mouse_move',
            pygame.MOUSEWHEEL: 'on_global_mouse_wheel',
            pygame.QUIT: 'on_quit',
            pygame.TEXTEDITING: 'on_text_editing',
            pygame.TEXTINPUT: 'on_text_input',
            pygame.VIDEOEXPOSE: 'on_video_expose',
            pygame.VIDEORESIZE: 'on_video_resize',
            pygame.WINDOWCLOSE: 'on_window_close',
            pygame.WINDOWENTER: 'on_global_mouse_enter',
            pygame.WINDOWEXPOSED: 'on_window_exposed',
            pygame.WINDOWFOCUSGAINED: 'on_window_focus_gained',
            pygame.WINDOWFOCUSLOST: 'on_window_focus_lost',
            pygame.WINDOWLEAVE: 'on_global_mouse_leave',
            pygame.WINDOWMAXIMIZED: 'on_window_maximized',
            pygame.WINDOWMINIMIZED: 'on_window_minimized',
            pygame.WINDOWMOVED: 'on_window_moved',
            pygame.WINDOWRESIZED: 'on_resize',
            pygame.WINDOWRESTORED: 'on_window_restored',
            pygame.WINDOWSIZECHANGED: 'on_window_size_changed',
            pygame.WINDOWSHOWN: 'on_window_shown',
            pygame.WINDOWHIDDEN: 'on_window_hidden',
            pygame.WINDOWHITTEST: 'on_window_hit_test',
            pygame.WINDOWTAKEFOCUS: 'on_window_take_focus'
        }
        self.hook_mouse = True
        self.is_focusable = True
        self.is_mouse_left_down = False
        self.is_mouse_enter = True
        self.scale_x, self.scale_y = 1.0, 1.0
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
        self.sort_child = self.child.sort
        self.last_cursor_pos = (0, 0)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name == 'scale_x':
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
        elif name == 'scroll_x':
            for child in self.child.child:
                if hasattr(child, '_scroll_x'):
                    child.set('_scroll_x', self.scroll_x)
        elif name == 'scroll_y':
            for child in self.child.child:
                if hasattr(child, '_scroll_y'):
                    child.set('_scroll_y', self.scroll_y)
        return self

    def process_events(self, events: list) -> list:
        for event in events:
            func = self.processes.get(event.type) or self.processes[0]
            getattr(self, '_' + func)(event, hasattr(self, func))
        return events

    def draw(
            self,
            delta: float
    ) -> None:
        for child in self.child.child:
            child.draw(self.surface, delta, self.scroll_x, self.scroll_y)

    def on_mouse_process(self, xy: tuple) -> tuple:
        return xy

    def _on_quit(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_quit()  # type: ignore

    def _on_resize(self, event: pygame.event.Event, bind: bool) -> None:
        self.w, self.h = event.x, event.y
        for child in self.child.child:
            if hasattr(child, 'fit_to_screen') and child.fit_to_screen:
                child.set('w', self.w).set('h', self.h)
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
        event.pos = self.on_mouse_process(event.pos)
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
            elif is_android:
                if hasattr(self.last_hover, '_on_mouse_leave'):
                    self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
                self.last_hover = self
                if hasattr(self.last_hover, '_on_mouse_enter'):
                    self.last_hover._on_mouse_enter(event, hasattr(self.last_hover, 'on_mouse_enter'))
            if hasattr(self, 'on_global_click'):
                self.on_global_click(event.pos)
        if bind:
            self.on_global_mouse_up(event.pos, event.button)  # type: ignore

    def _on_global_mouse_move(self, event: pygame.event.Event, bind: bool) -> None:
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

    def _on_global_mouse_enter(self, event: pygame.event.Event, bind: bool) -> None:
        self.is_mouse_enter = True
        event.pos = self.last_cursor_pos
        if bind:
            self.on_global_mouse_enter(event)  # type: ignore

    def _on_global_mouse_leave(self, event: pygame.event.Event, bind: bool) -> None:
        self.is_mouse_enter = False
        event.pos = self.last_cursor_pos
        if not self.is_mouse_left_down and not self.last_hover == self:
            self.last_hover._on_mouse_leave(event, hasattr(self.last_hover, 'on_mouse_leave'))
            self.last_hover = self
            self._on_mouse_leave(event, hasattr(self, 'on_mouse_leave'))
        if bind:
            self.on_global_mouse_leave(event)  # type: ignore

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

    def _on_window_close(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_close(event.window)  # type: ignore

    def _on_active(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_active(event.gain, event.state)  # type: ignore

    def _on_audio_device_added(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_audio_device_added(event.which, event.iscapture)  # type: ignore

    def _on_audio_device_removed(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_audio_device_removed(event.which, event.iscapture)  # type: ignore

    def _on_window_shown(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_shown(event.window)  # type: ignore

    def _on_window_focus_gained(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_focus_gained(event.window)  # type: ignore

    def _on_window_focus_lost(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_focus_lost(event.window)  # type: ignore

    def _on_text_editing(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_text_editing(event.text, event.start, event.length)  # type: ignore

    def _on_video_expose(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_video_expose()  # type: ignore

    def _on_window_exposed(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self._on_window_exposed(event.window)  # type: ignore

    def _on_window_moved(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_moved(event.x, event.y)  # type: ignore

    def _on_text_input(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_text_input(event.text)  # type: ignore

    def _on_video_resize(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_video_resize(event.w, event.h)  # type: ignore

    def _on_window_size_changed(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_size_changed(event.x, event.y)  # type: ignore

    def _on_window_maximized(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_maximized(event.window)  # type: ignore

    def _on_window_restored(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_restored(event.window)  # type: ignore

    def _on_window_minimized(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_minimized(event.window)  # type: ignore

    def _on_window_hidden(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_hidden(event.window)  # type: ignore

    def _on_window_take_focus(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_take_focus(event.window)  # type: ignore

    def _on_window_hit_test(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_window_hit_test(event.window)  # type: ignore

    def _on_unknown_event(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_unknown_event(event)  # type: ignore
