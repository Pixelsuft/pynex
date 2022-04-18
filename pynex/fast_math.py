import math
import numba  # type: ignore


@numba.njit(fastmath=True)
def try_sqrt(number: any) -> float:
    try:
        return math.sqrt(number)
    except ValueError:
        return 0.0


@numba.njit(fastmath=True)
def is_colliding_rect(rect: any, xy: tuple, offset_x: int = 0, offset_y: int = 0) -> bool:
    return rect[2] + rect[0] + offset_x > xy[0] >= rect[0] + offset_x and\
           rect[3] + rect[1] + offset_y > xy[1] >= rect[1] + offset_y


def is_colliding(child: any, xy: tuple, offset_x: int = 0, offset_y: int = 0) -> bool:
    return is_colliding_rect((child.x, child.y, child.w, child.h), xy, offset_x, offset_y)


@numba.njit(fastmath=True)
def normalise_rotation(rotation: any) -> any:
    while rotation >= 360:
        rotation -= 360
    while rotation < 0:
        rotation += 360
    return rotation


@numba.njit(fastmath=True)
def calc_rotation(x_offset: float, y_offset: float, diagonal: float = None) -> float:
    if not diagonal:
        diagonal = math.sqrt(x_offset * x_offset + y_offset * y_offset)
    if x_offset >= 0:
        if y_offset >= 0:  # bottom right
            return 90 / diagonal * x_offset + 180
        else:  # top right
            return 360 - 90 / diagonal * x_offset
    else:
        if y_offset >= 0:  # bottom left
            return 180 + 90 / diagonal * x_offset
        else:  # top left
            return -90 / diagonal * x_offset


@numba.njit(fastmath=True)
def calc_offset(rotation: float, diagonal: float) -> tuple:
    if rotation >= 270:  # top right
        x_offset = diagonal / 90 * (360 - rotation)
        return x_offset, math.sqrt(diagonal * diagonal - x_offset * x_offset)
    elif rotation >= 90:  # bottom left + right
        x_offset = diagonal / 90 * (rotation - 180)
        return x_offset, math.sqrt(diagonal * diagonal - x_offset * x_offset)
    else:  # top left
        x_offset = diagonal / 90 * rotation
        return -x_offset, -math.sqrt(diagonal * diagonal - x_offset * x_offset)
