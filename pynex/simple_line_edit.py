import pygame
from . import *


class NSimpleLineEdit:
    def __init__(
            self,
            parent: any,
            font: NFont,
            font_size: int,
            xy: tuple,
            text: str = '',
            color: tuple = (0, 0, 0),
            blink_time: float = 0.75,
            bg_color: tuple = (0, 0, 0),
            show_bg: bool = False,
            auto_size: bool = True,
            anti_alias: bool = True,
            stretch: bool = False
    ) -> None:
        super(NSimpleLineEdit, self).__init__()
        self.font_size = font_size
        self.font: NChildFont = font.create_size(self.font_size)
        self.x, self.y = xy
        self.w, self.h = 0, 0
        self._width, self._height = self.w, self.h
        self.anti_alias = anti_alias
        self.auto_size = auto_size
        self.show_bg = show_bg
        self.stretch = stretch
        self.hook_mouse = True
        self.is_visible = True
        self.is_enabled = True
        self.is_focusable = True
        self.enable_scroll = True
        self.auto_scale = True
        self.scale_x = self.scale_y = self.min_scale = self.max_scale = self.avg_scale = 1.0
        self.usable = True
        self.blink_symbol = '|'
        self.no_blink_symbol = ' '
        self.blink = self.no_blink_symbol
        self.blink_time = blink_time
        self.text = text
        self.x_offset = 0
        self.y_offset = 0
        self.blink_pos = 0
        self.bg_border_radius = 0
        self.multi_lines_align = LABEL_ALIGN_LEFT
        self.surface: pygame.Surface = None  # type: ignore
        self.timer = NTimer(None, self.blink_time, auto_start=False).set('on_tick', self.on_blink_tick)
        self.cursor = get_system_cursor('IBEAM')
        self.color = color
        self.bg_color = bg_color
        self.z_order = 0
        self.tag = ''
        self.id = ''
        self.set('text', text)
        if parent:
            parent.add_child(self)

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        if name == 'text':
            self.blink_pos = len(value)
        if name in ('text', 'color', 'anti_alias', 'mutli_line_align', 'stretch', 'auto_size'):
            self.redraw(self.text)
        elif name in ('font', 'font_size'):
            self.font = self.font.create_size(self.font_size)
            self.redraw(self.text)
        elif name in ('scale_x', 'scale_y'):
            self.font.scale(self.avg_scale)
            self.redraw(self.text)
        return self

    def redraw(self, text: str) -> None:
        if text.count('\n') > 0:
            text = text.replace('\n', '')
        self.surface = self.font.render(
            text[:self.blink_pos] + self.blink + text[self.blink_pos:],
            self.anti_alias,
            self.color
        )
        self._width, self._height = self.surface.get_size()
        if self.auto_size:
            self.w, self.h = r(self._width / self.avg_scale), r(self._height / self.avg_scale)
        elif self.stretch:
            self.surface = pygame.transform.scale(
                self.surface, round_tuple((self.w * self.scale_x, self.h * self.scale_y))
            )
        return

    def draw(self, surface: pygame.Surface, delta: float, scroll_x: int, scroll_y: int) -> None:
        if not self.is_visible:
            return
        self.timer.draw(surface, delta, scroll_x, scroll_y)
        if not self.enable_scroll:
            scroll_x = scroll_y = 0
        if self.show_bg:
            pygame.draw.rect(
                surface,
                self.bg_color,
                round_tuple((self.x * self.scale_x + scroll_x, self.y * self.scale_y + scroll_y,
                             self.w * self.scale_x, self.h * self.scale_y)),
                0,
                r(self.bg_border_radius * self.avg_scale)
            )
        surface.blit(
            self.surface,
            round_tuple(((self.x + self.x_offset) * self.scale_x + scroll_x,
                         (self.y + self.y_offset) * self.scale_y + scroll_y)),
            None if self.auto_size else (0, 0, r((self.w - 1) * self.scale_x), r(self.h * self.scale_y))
        )

    def on_blink_tick(self, delta: float) -> None:
        self.blink = self.no_blink_symbol if self.blink == self.blink_symbol else self.blink_symbol
        self.redraw(self.text)

    def process_key(self, event: pygame.event.Event, text: str) -> None:
        if event.key == pygame.K_BACKSPACE:
            self.timer.current_rate = 0.0
            self.blink = self.blink_symbol
            if len(text) > 0:
                self.text = self.text[:self.blink_pos - 1] + self.text[self.blink_pos:]
                self.blink_pos -= 1
        elif event.key == pygame.K_RIGHT:
            if len(self.text) > self.blink_pos:
                self.blink_pos += 1
        elif event.key == pygame.K_LEFT:
            if self.blink_pos > 0:
                self.blink_pos -= 1
        elif event.key == pygame.K_DELETE:
            self.text = self.text[:self.blink_pos] + self.text[self.blink_pos + 1:]
        elif event.unicode:
            self.timer.current_rate = 0.0
            self.blink = self.no_blink_symbol
            self.text = self.text[:self.blink_pos] + event.unicode + self.text[self.blink_pos:]
            self.blink_pos += len(event.unicode)

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
        self.blink = self.blink_symbol
        self.redraw(self.text)
        self.timer.run()
        pygame.key.start_text_input()
        if bind:
            self.on_focus_enter(event.pos, event.button)  # type: ignore

    def _on_focus_leave(self, event: pygame.event.Event, bind: bool) -> None:
        pygame.key.stop_text_input()
        self.timer.stop()
        self.timer.current_rate = 0.0
        self.blink = self.no_blink_symbol
        self.redraw(self.text)
        if bind:
            self.on_focus_leave(event.pos, event.button)  # type: ignore

    def _on_key_down(self, event: pygame.event.Event, bind: bool) -> None:
        self.process_key(event, self.text)
        self.redraw(self.text)
        if bind:
            self.on_key_down(event)  # type: ignore

    def _on_key_up(self, event: pygame.event.Event, bind: bool) -> None:
        if bind:
            self.on_key_up(event)  # type: ignore
