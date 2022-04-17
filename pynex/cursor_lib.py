import pygame
from . import *


cursors = {

}
system_cursors = {

}


def compile_cursors() -> None:
    for _cursor in dir(pygame):
        if not _cursor.startswith('SYSTEM_CURSOR'):
            continue
        system_cursors[_cursor[14:]] = getattr(pygame, _cursor)

    cursors['DEFAULT'] = pygame.mouse.get_cursor()
    cursors['EMPTY'] = pygame.cursors.Cursor((8, 8), (0, 0), *pygame.cursors.compile((
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
    )))


def get_system_cursor(cursor_name: str) -> pygame.Cursor:
    return system_cursors.get(cursor_name) or cursors.get('default')
