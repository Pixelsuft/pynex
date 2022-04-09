import time
import random
import math
import pynex
import pygame


# Init
pynex.request_android_default_permissions()
pygame.init()

# Create window and main frame
display_flags = pygame.RESIZABLE | pynex.FORCE_FULL_SCREEN  # | pygame.DOUBLEBUF
screen = pygame.display.set_mode((800, 600), display_flags)
main_window = pynex.NMainFrame(screen)
pygame.display.set_caption('Pixelsuft pynex example')

# Load things
font = pynex.NFont(pynex.p('example_files', 'segoeuib.ttf')).set('scale_slow_fix', True)
image = pygame.image.load(pynex.p('example_files', 'win7_logo_transparent.png')).convert_alpha()
pixelsuft_image = pygame.image.load(pynex.p('example_files', 'pixelsuft.png')).convert_alpha()
python_image = pygame.image.load(pynex.p('example_files', 'python.png')).convert_alpha()
pygame.display.set_icon(python_image)

# Vars
running = True
clear_bg = True
anti_alias = True
global_scale = 1.0
dpi = pynex.get_dpi()
images_to_set = (image, python_image, pixelsuft_image)
image_rot_right = bool(random.randint(0, 1))

# Create label object with events
pynex.NLabel(
    main_window,
    font,
    36,
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
    font,
    24,
    (0, 150),
    '',
    (255, 0, 0)
).set('id', 'l2').set('z_order', 1).set('is_enabled', False)

# Create label object for FPS
fps_label = pynex.NLabel(main_window, font, 24, (0, 0), 'FPS: 0', (0, 0, 255))\
    .set('z_order', 999).set('enable_scroll', False).set('is_enabled', False)


def update_info(*args):
    res = screen.get_size()
    res_gcd = math.gcd(res[0], res[1])
    info_label.set('text', f'''DPI: {dpi}
RES: {res[0]}x{res[1]} ({round(res[0] / res_gcd)}:{round(res[1] / res_gcd)})
SCROLL: {(main_window.scroll_x, main_window.scroll_y)}
SPEED HACK VALUE: {round(main_window.find_by_id('s1').value * 100) / 100}
IMAGE VALUE: {round(main_window.find_by_id('s2').value) + 1}
SCALE VALUE: {round(global_scale * 10) / 10}
ANTI ALIASING: {anti_alias}''')


def toggle_clear_bg(current_state):
    global clear_bg
    clear_bg = current_state


def toggle_time_monotonic(current_state):
    clock.set('time_func', time.monotonic if current_state else time.time)


def toggle_vsync(current_state):
    pygame.display.set_mode(
        screen.get_size(),
        display_flags | (pygame.SCALED if current_state else 0),  # From pygame
        vsync=int(current_state)
    )
    update_info()


def change_button_text_pos(pos):
    button = main_window.find_by_id('b1')
    button.set('text', button.text[-1] + button.text[:-1])


def on_quit():
    global running
    running = False


def on_mouse_move(pos, rel, buttons, touch):
    if not main_window.is_mouse_left_down:
        return
    main_window.scroll_x += round(rel[0])
    main_window.scroll_y += round(rel[1])
    update_info()


def on_mouse_wheel(rel, touch, flipped):
    main_window.scroll_x += round(rel[0] * 5)
    main_window.scroll_y += round(rel[1] * 5)
    update_info()


def make_screenshot(pos):
    if not pynex.is_android:
        pynex.surface_to_image(screen).show()
        return
    try:
        pynex.surface_to_image(screen).save('/storage/emulated/0/pynex.png', 'PNG')
        main_window.find_by_id('b2').set('text', 'Saved to pynex.png')
    except Exception as _err:
        del _err
        main_window.find_by_id('b2').set('text', 'Failed to save!')


def with_dpi(pos):
    global global_scale
    main_window.find_by_id('c3').set('checked', False)
    if dpi > 0:
        default_dpi = 240 if pynex.is_android else 96
        global_scale = dpi / default_dpi
        main_window.set('scale_x', global_scale).set('scale_y', global_scale)
    update_info()


def choose_speed_hack(val):
    clock.set('speed_hack', val)
    update_info()


def update_image(val):
    img.set('image', images_to_set[round(val)])
    update_info()


def change_global_scale(multiplier):
    global global_scale
    global_scale += multiplier * 0.1
    if global_scale < 0.5:
        global_scale = 0.5
    global_scale = round(global_scale * 10) / 10
    main_window.set('scale_x', global_scale).set('scale_y', global_scale)
    update_info()


def toggle_anti_alias(pos):
    global anti_alias
    anti_alias = not anti_alias
    for child in main_window.child.get_child():
        if hasattr(child, 'anti_alias'):
            child.set('anti_alias', anti_alias)
    update_info()


# Create image object
img = pynex.NImage(
    main_window,
    images_to_set[0],
    (0, 150),
    auto_size=False,
    stretch=True
).set('w', 350).set('h', 350).set('z_order', -1).set('id', 'i1').set('hook_mouse', False)

# Create button object
pynex.NWinAnimatedButton(
    main_window,
    font,
    24,
    (300, 100),
    'Hello, world!\nAgain Hello!',
    (150, 40),
    (0, 0, 0),
    auto_size=True
).set('id', 'b1').set('z_order', 2).set('on_click', change_button_text_pos)

# Create button object for screenshot
pynex.NWinAnimatedButton(
    main_window,
    font,
    24,
    (300, 240),
    'Make Screenshot!',
    (150, 40),
    (0, 0, 0),
    auto_size=True
).set('id', 'b2').set('z_order', 2).set('on_click', make_screenshot)

# Create button object for dpi scale
pynex.NWinAnimatedButton(
    main_window,
    font,
    24,
    (300, 300),
    'Scale by DPI!',
    (150, 40),
    (0, 0, 0),
    auto_size=True
).set('id', 'b3').set('z_order', 2).set('on_click', with_dpi)

# Create check box object for clearing bg
pynex.NAnimatedCheckBox(
    main_window,
    font,
    24,
    (200, 0),
    'Fill Background',
    (255, 0, 0),
    auto_size_box=True
).set('checked', True).set('z_order', 3).set('border_radius', 3).set('on_check', toggle_clear_bg)

# Create check box object for time.monotonic
pynex.NAnimatedCheckBox(
    main_window,
    font,
    24,
    (200, 40),
    'time.monotonic',
    (255, 0, 0),
    auto_size_box=True
).set('z_order', 3).set('border_radius', 3).set('on_check', toggle_time_monotonic)

# Create check box object for time.monotonic
pynex.NAnimatedCheckBox(
    main_window,
    font,
    24,
    (450, 0),
    'Vertical Sync',
    (255, 0, 0),
    auto_size_box=True
).set('id', 'c3').set('z_order', 3).set('border_radius', 3).set('on_check', toggle_vsync)

# Create edit object
pynex.NSimpleLineEdit(
    main_window,
    font,
    24,
    (300, 200),
    'Hello, world!',
    (0, 0, 0),
    0.5,
    (225, 225, 225),
    True,
    False
).set('z_order', 4).set('w', 400).set('h', 32)

# Create slider object for speed hack
pynex.NHorizontalSlider(
    main_window,
    (600, 350),
    min_value=0.25,
    max_value=10,
    value=1
).set('z_order', 5).set('id', 's1').set('on_change', choose_speed_hack).set('page_step', 0.25)

# Create slider object for changing image
image_changer = pynex.NVerticalSlider(
    main_window,
    (700, 150),
    value=0,
    min_value=0,
    max_value=len(images_to_set) - 1
).set('z_order', 5).set('id', 's2').set('on_change', update_image).set('page_step', 1)

# Create bar object for SIN
sin_bar = pynex.NProgressBar(
    main_window,
    (300, 350),
    (160, 22),
    min_value=-1,
    max_value=1
).set('z_order', 5).set('is_enabled', False)

# Create bar object for COS
cos_bar = pynex.NProgressBar(
    main_window,
    (300, 400),
    (160, 22),
    min_value=-1,
    max_value=1
).set('z_order', 5).set('is_enabled', False)

# Create buttons for scaling
pynex.NWinAnimatedButton(
    main_window,
    font,
    24,
    (470, 350),
    '+',
    (50, 50)
).set('z_order', 2).set('on_click', lambda pos: change_global_scale(1))
pynex.NWinAnimatedButton(
    main_window,
    font,
    24,
    (530, 350),
    '-',
    (50, 50)
).set('z_order', 2).set('on_click', lambda pos: change_global_scale(-1))

# Create Button For Anti Alias
pynex.NWinAnimatedButton(
    main_window,
    font,
    24,
    (300, 450),
    'Toggle AntiAliasing',
    (150, 40),
    auto_size=True
).set('z_order', 2).set('on_click', toggle_anti_alias)

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
clock = pynex.NFps(60, unlocked=True)

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
    img.set('rotation', img.rotation + 50 * clock.delta * (-clock.speed_hack if image_rot_right else clock.speed_hack))
    sin_bar.set('value', math.sin(clock.last_tick))
    cos_bar.set('value', math.cos(clock.last_tick))
    fps_label.set('text', f'FPS: {clock.get_fps_int()}')
    main_window.draw(clock.delta)
    pygame.display.flip()

pygame.quit()
