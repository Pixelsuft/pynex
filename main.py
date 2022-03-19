import time
import random
import math
import pynex
import pygame


# Init
pynex.request_android_default_permissions()
pygame.init()

# Create window and main frame
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE | pynex.FORCE_FULL_SCREEN)
main_window = pynex.NMainFrame(screen)
pygame.display.set_caption('Pixelsuft pynex example')

# Load things
font36 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 36)
font24 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 24)
font12 = pygame.font.Font(pynex.p('example_files', 'segoeuib.ttf'), 12)
image = pygame.image.load(pynex.p('example_files', 'win7_logo_transparent.png')).convert_alpha()
python_image = pygame.transform.scale(
    pygame.image.load(pynex.p('example_files', 'python.png')).convert_alpha(), (500, 498)
)
pygame.display.set_icon(python_image)

# Vars
running = True
clear_bg = True
need_id = 0
template = '''DPI: %dpi%
RES: %res%
SCROLL: %scroll%
SPEED HACK VALUE: %s1%
IMAGE VALUE: %s2%'''
dpi = pynex.get_dpi()
images_to_set = (image, python_image)
image_rot_right = bool(random.randint(0, 1))
image_rotation = 0

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
).set('id', 'l2').set('z_order', 1).set('is_enabled', False)

# Create label object for FPS
fps_label = pynex.NLabel(main_window, font24, (0, 0), 'FPS: 0', (0, 0, 255))\
    .set('z_order', 999).set('enable_scroll', False).set('is_enabled', False)


def update_info(*args):
    info_label.set('text', template.replace('%dpi%', str(dpi)).replace('%res%', str(screen.get_size()))\
                   .replace('%scroll%', str((main_window.scroll_x, main_window.scroll_y)))\
                   .replace('%s1%', str(round(main_window.find_by_id('s1').value * 100) / 100))\
                   .replace('%s2%', str(round(main_window.find_by_id('s2').value))))


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
        return
    try:
        pynex.surface_to_image(screen).save('/storage/emulated/0/pynex.png', 'PNG')
        main_window.find_by_id('b2').set('text', 'Saved to\n/storage/emulated/0/pynex.png')
    except Exception as _err:
        if _err:
            'PyCharm Hide Warning'
        main_window.find_by_id('b2').set('text', 'Failed to save!')


def with_dpi(pos):
    if dpi > 0:
        default_dpi = 240 if pynex.is_android else 96
        new_width = round(screen.get_width() * default_dpi / dpi)
        new_height = round(screen.get_height() * default_dpi / dpi)
        pygame.display.set_mode(
            (new_width, new_height),
            pygame.RESIZABLE | pynex.FORCE_FULL_SCREEN | pynex.FORCE_SCALED
        )
    main_window.find_by_id('b3').set('is_enabled', False)
    update_info()


def choose_speed_hack(val):
    clock.set('speed_hack', val)
    update_info()


# Create image object
img = pynex.NImage(
    main_window,
    images_to_set[0],
    (0, 150)
).set('z_order', -1).set('id', 'i1').set('hook_mouse', False)

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
    (400, 240),
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
    (400, 300),
    'Scale by DPI! (Android)',
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
).set('z_order', 5).set('id', 's1').set('on_change', choose_speed_hack)

# Create slider object for changing image
image_changer = pynex.NVerticalSlider(
    main_window,
    (600, 400),
    value=0,
    min_value=0,
    max_value=len(images_to_set) - 1
).set('z_order', 5).set('id', 's2').set('on_change', update_info)

# Create slider object for SIN
sin_slider = pynex.NHorizontalSlider(
    main_window,
    (300, 350),
    min_value=-1,
    max_value=1
).set('z_order', 5).set('is_enabled', False)

# Create slider object for COS
cos_slider = pynex.NHorizontalSlider(
    main_window,
    (300, 400),
    min_value=-1,
    max_value=1
).set('z_order', 5).set('is_enabled', False)

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
    if image_rot_right:
        image_rotation -= 50 * clock.delta * clock.speed_hack
        while image_rotation <= 0:
            image_rotation += 360
    else:
        image_rotation += 50 * clock.delta * clock.speed_hack
        while image_rotation >= 360:
            image_rotation -= 360
    img.set(
        'image',
        pygame.transform.rotate(images_to_set[round(image_changer.value)], round(image_rotation))
    )
    sin_slider.set('value', math.sin(clock.last_tick))
    cos_slider.set('value', math.cos(clock.last_tick))
    fps_label.set('text', f'FPS: {clock.get_fps_int()}')
    main_window.draw(clock.delta)
    pygame.display.flip()

pygame.quit()
