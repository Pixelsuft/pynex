import os
import sys
import random
import pygame
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
    if os.getenv('PYNEX_NO_NUMBA'):
        raise RuntimeError('No Numba')
    import numba  # type: ignore
    from .slow_math import *
    from .fast_math import *
    is_numba = True
except Exception as _err:
    del _err
    from .slow_math import *
    is_numba = False
try:
    import win32api  # type: ignore
    import win32gui  # type: ignore
    import win32con  # type: ignore
    import win32print  # type: ignore
    is_winapi = True
except ImportError:
    is_winapi = False


r = round
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


def get_java_class(class_name: any, include_protected: bool = True, include_private: bool = True) -> any:
    if not is_jni:
        raise RuntimeError('JNI is not running!')
    return jnius.autoclass(class_name, include_protected, include_private)


def get_dpi() -> int:
    if is_android:
        try:
            return get_java_class('android.util.DisplayMetrics')().getDeviceDensity()
        except RuntimeError:
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


def random_color(min_color: int = 0, max_color: int = 255, use_alpha: bool = False) -> tuple:
    return tuple(
        random.randint(min_color, max_color) for _x in range(4 if use_alpha else 3)
    )


def load_style_luna(path: str, chroma_key: tuple = None, max_height: int = None) -> dict:
    result = {}
    for file_name in os.listdir(path):
        file_no_ext = '.'.join(file_name.split('.')[:-1]).lower()
        if 'preview' in file_no_ext:
            continue
        image = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
        if chroma_key and file_no_ext in ('lt', 'mtl', 'mtr', 'rt'):
            for _x in range(image.get_width()):
                for _y in range(max_height or image.get_height()):
                    if image.get_at((_x, _y)) == chroma_key:
                        image.set_at((_x, _y), (0, 0, 0, 0))
        result[file_no_ext] = image
    return result
