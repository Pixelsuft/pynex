import os
import sys
import pygame
import random
import ctypes
from PIL import Image
try:
    import android  # type: ignore
    from android.permissions import request_permissions  # type: ignore
    from android.permissions import Permission  # type: ignore
    is_android = True
except ImportError:
    is_android = False
try:
    import jnius  # type: ignore
    is_jni = True
except Exception as _err:
    del _err
    is_jni = False
try:
    import win32api  # type: ignore
    import win32gui  # type: ignore
    import win32con  # type: ignore
    import win32print  # type: ignore
    is_winapi = True
except ImportError:
    is_winapi = False


encoding = sys.getdefaultencoding()
is_windows = not is_android and hasattr(ctypes, 'windll')
cur_path = os.getcwd()


def request_android_default_permissions() -> None:
    if not is_android:
        return
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])


def round_tuple(_tuple: any) -> tuple:
    return tuple(round(_x) for _x in _tuple)


def round_tuples(_tuple: any) -> tuple:
    return tuple(round_tuple(_x) for _x in _tuple)


def random_float(a: float, b: float) -> float:
    return random.random() * (b - a) + a


def get_dpi() -> int:
    if is_android:
        if is_jni:
            return jnius.autoclass('android.util.DisplayMetrics')().getDeviceDensity()
        return 240
    if is_windows and is_winapi:
        hdc = win32gui.GetDC(0)
        result = max(
            win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX),
            win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSY)
        )
        return result
    return 96


def p(*path) -> str:
    return os.path.join(cur_path, *path)


def image_to_surface(image: Image.Image) -> pygame.Surface:
    return pygame.image.frombuffer(
        image.tobytes(),
        image.size,
        image.mode  # type: ignore
    )


def surface_to_image(surface: pygame.Surface, is_flipped: bool = False) -> Image.Image:
    img_mode = 'RGB' if surface.get_alpha() is None else 'RGBA'
    return Image.frombytes(
        img_mode,  # type: ignore
        surface.get_size(),
        pygame.image.tostring(
            surface,
            img_mode,  # type: ignore
            is_flipped
        )
    )


def is_colliding(child: any, xy: tuple, offset_x: int = 0, offset_y: int = 0) -> bool:
    return child.w + child.x + offset_x > xy[0] >= child.x + offset_x and\
           child.h + child.y + offset_y > xy[1] >= child.y + offset_y


def is_colliding_rect(rect: any, xy: tuple, offset_x: int = 0, offset_y: int = 0) -> bool:
    return rect[2] + rect[0] + offset_x > xy[0] >= rect[0] + offset_x and\
           rect[3] + rect[1] + offset_y > xy[1] >= rect[1] + offset_y


def random_color(use_alpha: bool = False) -> tuple:
    return tuple(
        random.randint(0, 255) for _x in range(4 if use_alpha else 3)
    )
