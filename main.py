import pynex
import pygame


pynex.request_android_default_permissions()
pygame.init()

screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE | pynex.FORCE_FULL_SCREEN)
main_window = pynex.NMainFrame(screen)
pygame.display.set_caption('Pixelsuft pynex')

font36 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 36)
font24 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 24)
image = pygame.image.load(pynex.p('example_files', 'win7_logo_transparent.png')).convert_alpha()

running = True
clear_bg = True

pynex.NLabel(
    main_window,
    font36,
    (0, 50),
    'Hello, world!',
    (0, 255, 0)
).set('id', 'l1').set('z_order', 1).set('bg_border_radius', 5).set(
    'on_mouse_enter',
    lambda *args: main_window.find_by_id('l1').set('bg_color', pynex.random_color()).set('show_bg', True)
).set('on_mouse_leave', lambda *args: main_window.find_by_id('l1').set('show_bg', False)).set(
        'on_click',
        lambda *args: main_window.find_by_id('l1').set('text', f'Hello, world!\n{round(pynex.random_float(10, 1000))}')
).set('cursor', pynex.system_cursors.get('HAND')).set('multi_lines_align', pynex.LABEL_ALIGN_CENTER)

fps_label = pynex.NLabel(main_window, font24, (0, 0), 'FPS: 0', (0, 0, 255))\
    .set('z_order', 999).set('enable_scroll', False)


def toggle_clear_bg(current_state):
    global clear_bg
    clear_bg = current_state


def change_button_text_pos(pos):
    button = main_window.find_by_id('b1')
    button.set('text', button.text[-1] + button.text[:-1])


def on_quit():
    global running
    running = False


def on_mouse_move(pos, rel, buttons, touch):
    if not main_window.is_mouse_left_down:
        return
    main_window.scroll_x += rel[0]
    main_window.scroll_y += rel[1]


def on_mouse_wheel(rel, touch, flipped) -> None:
    main_window.scroll_x += rel[0] * 5
    main_window.scroll_y += rel[1] * 5


pynex.NImage(
    main_window,
    image,
    (0, 150)
).set('z_order', -1).set('hook_mouse', False)

pynex.NWinAnimatedButton(
    main_window,
    font24,
    (300, 100),
    'Hello, world!\nAgain Hello!',
    (150, 40),
    (0, 0, 0),
    animation_time=0.2,
    auto_size=True
).set('id', 'b1').set('z_order', 2).set('on_click', change_button_text_pos)

pynex.NCheckBoxAnimated(
    main_window,
    font24,
    (200, 0),
    'Clear Background',
    (255, 0, 0),
    auto_size_box=True
).set('checked', True).set('z_order', 3).set('border_radius', 3).set('on_check', toggle_clear_bg)

pynex.NSimpleLineEdit(
    main_window,
    font24,
    (200, 200),
    'Hello, world',
    (0, 0, 0),
    0.5,
    (225, 225, 225),
    True,
    False
).set('z_order', 4).set('w', 400).set('h', 32)

color_fade = pynex.NSimpleColorFade(
    main_window,
    time=10 if pynex.is_android else 3,
    from_color=pynex.random_color(),
    to_color=(240, 240, 240)
)

main_window.sort_child()
main_window.set('on_quit', on_quit).set('on_mouse_move', on_mouse_move).set('on_mouse_wheel', on_mouse_wheel)
clock = pynex.NFps(60, unlocked=True)

while running:
    main_window.process_events(pygame.event.get())
    if not clock.tick():
        continue
    if clear_bg:
        screen.fill(color_fade.color)
    fps_label.set('text', f'FPS: {clock.get_fps_int()}')
    main_window.draw(clock.delta)
    pygame.display.flip()

pygame.quit()
