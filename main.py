import time
import random
import pynex
import pygame


# Init
pynex.request_android_default_permissions()
pygame.init()

# Create window and main frame
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE | pynex.FORCE_FULL_SCREEN)
main_window = pynex.NMainFrame(screen)
pygame.display.set_caption('Pixelsuft pynex')

# Load things
font36 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 36)
font24 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 24)
font12 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 12)
image = pygame.image.load(pynex.p('example_files', 'win7_logo_transparent.png')).convert_alpha()

# Vars
running = True
clear_bg = True
template = '''DPI: %dpi%
RES: %res%
SCROLL: %scroll%'''
dpi = pynex.get_dpi()

# Create label object with events
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

# Create info label
info_label = pynex.NLabel(
    main_window,
    font24,
    (0, 150),
    template,
    (255, 0, 0)
).set('id', 'l2').set('z_order', 1)

# Create label object for FPS
fps_label = pynex.NLabel(main_window, font24, (0, 0), 'FPS: 0', (0, 0, 255))\
    .set('z_order', 999).set('enable_scroll', False)


def update_info(*args):
    info_label.set('text', template.replace('%dpi%', str(dpi)).replace('%res%', str(screen.get_size()))\
                   .replace('%scroll%', str((main_window.scroll_x, main_window.scroll_y))))


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
    update_info()


def on_mouse_wheel(rel, touch, flipped):
    main_window.scroll_x += rel[0] * 5
    main_window.scroll_y += rel[1] * 5
    update_info()


def make_screenshot(pos):
    if not pynex.is_android:
        pynex.surface_to_image(screen).show()
    try:
        pynex.surface_to_image(screen).save('/storage/emulated/0/pynex.png', 'PNG')
        main_window.find_by_id('b2').set('text', 'Saved to\n/storage/emulated/0/pynex.png')
    except Exception as _err:
        if _err:
            'PyCharm Hide Warning'
        main_window.find_by_id('b2').set('text', 'Failed to save!')


def with_dpi(pos):
    last_width, last_height = screen.get_size()
    update_info()


# Create image object
img = pynex.NImage(
    main_window,
    image,
    (0, 150)
).set('z_order', -1).set('hook_mouse', False)

# Create button object
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

# Create button object for screenshot
pynex.NWinAnimatedButton(
    main_window,
    font24,
    (400, 300),
    'Make Screenshot!',
    (150, 40),
    (0, 0, 0),
    animation_time=0.2,
    auto_size=True
).set('id', 'b2').set('z_order', 2).set('on_click', make_screenshot)

# Create button object for dpi scale
pynex.NWinAnimatedButton(
    main_window,
    font24,
    (400, 400),
    'Scale by DPI!',
    (150, 40),
    (0, 0, 0),
    animation_time=0.2,
    auto_size=True
).set('id', 'b3').set('z_order', 2).set('on_click', with_dpi)

# Create check box object
pynex.NAnimatedCheckBox(
    main_window,
    font24,
    (200, 0),
    'Clear Background',
    (255, 0, 0),
    auto_size_box=True
).set('checked', True).set('z_order', 3).set('border_radius', 3).set('on_check', toggle_clear_bg)

# Create edit object
pynex.NSimpleLineEdit(
    main_window,
    font24,
    (300, 200),
    'Hello, world',
    (0, 0, 0),
    0.5,
    (225, 225, 225),
    True,
    False
).set('z_order', 4).set('w', 400).set('h', 32)

# Create color fade object for background
color_fade = pynex.NSimpleColorFade(
    main_window,
    time=3,
    from_color=pynex.random_color(),
    to_color=(240, 240, 240)
)

update_info()
# Sort child by Z order
main_window.sort_child()
main_window.set('on_quit', on_quit).set('on_mouse_move', on_mouse_move).set('on_mouse_wheel', on_mouse_wheel)\
    .set('on_resize', update_info)
# Create FPS clock (time.time for windows, because time.monotonic is limited to 60 FPS on it (why?))
clock = pynex.NFps(60, unlocked=True, time_function=time.time if pynex.is_windows else time.monotonic)

while running:
    main_window.process_events(pygame.event.get())
    if not clock.tick():
        continue
    if not color_fade.is_enabled:
        color_fade.create(
            time=random.randint(3, 10),
            from_color=color_fade.color,
            to_color=pynex.random_color()
        )
    if clear_bg:
        screen.fill(color_fade.color)
    img.set('image', pygame.transform.rotate(image, (clock.last_tick * 100) % 360))
    fps_label.set('text', f'FPS: {clock.get_fps_int()}')
    main_window.draw(clock.delta)
    pygame.display.flip()

pygame.quit()
