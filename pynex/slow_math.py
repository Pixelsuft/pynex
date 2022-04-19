import math


def try_sqrt(number: any) -> float:
    try:
        return math.sqrt(number)
    except ValueError:
        return 0.0


def is_colliding(child: any, xy: tuple, offset_x: int = 0, offset_y: int = 0) -> bool:
    return (child.w + child.x) * child.scale_x + offset_x > xy[0] >= child.x * child.scale_x + offset_x and \
           (child.h + child.y) * child.scale_y + offset_y > xy[1] >= child.y * child.scale_y + offset_y


def is_colliding_rect(rect: any, xy: tuple, offset_x: int = 0, offset_y: int = 0) -> bool:
    return rect[2] + rect[0] + offset_x > xy[0] >= rect[0] + offset_x and\
           rect[3] + rect[1] + offset_y > xy[1] >= rect[1] + offset_y


def normalise_rotation(rotation: any) -> any:
    while rotation >= 360:
        rotation -= 360
    while rotation < 0:
        rotation += 360
    return rotation


def calc_rotation(x_offset: float, y_offset: float) -> float:
    try:
        if x_offset >= 0:
            if y_offset >= 0:  # bottom right
                return 180 + 90 / (x_offset + y_offset) * x_offset
            else:  # top right
                return 360 - 90 / (x_offset - y_offset) * x_offset
        else:
            if y_offset >= 0:  # bottom left
                return 180 - 90 / (x_offset - y_offset) * x_offset
            else:  # top left
                return 90 / (x_offset + y_offset) * x_offset
    except ZeroDivisionError:
        return 0.0


def calc_offset(rotation: float, diagonal: float) -> tuple:
    try:
        if rotation >= 270:  # top right
            x_offset = diagonal / 90 * (360 - rotation)
            return x_offset, -try_sqrt(diagonal * diagonal - x_offset * x_offset)
        elif rotation >= 90:  # bottom left + right
            x_offset = diagonal / 90 * (rotation - 180)
            return x_offset, try_sqrt(diagonal * diagonal - x_offset * x_offset)
        else:  # top left
            x_offset = diagonal / 90 * rotation
            return -x_offset, -try_sqrt(diagonal * diagonal - x_offset * x_offset)
    except ZeroDivisionError:
        return 0.0, 0.0
