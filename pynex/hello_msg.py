import os
import sys


is_already_inited = sys.modules.get('pygame') is not None
hide_msg = os.getenv('PYGAME_HIDE_SUPPORT_PROMPT') is not None
if is_already_inited:
    if not hide_msg:
        print('pynex integrated')
elif not hide_msg:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'
    import pygame  # type: ignore
    os.unsetenv('PYGAME_HIDE_SUPPORT_PROMPT')
    print('pygame {} (SDL {}.{}.{}, Python {}.{}.{}, PyNex)'.format(
        pygame.ver, *pygame.get_sdl_version() + sys.version_info[0:3]
    ))
    print('Hello from the pygame community. https://www.pygame.org/contribute.html')
__all__ = ()
