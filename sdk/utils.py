from dataclasses import dataclass


@dataclass
class Vec3:
    x: float
    y: float
    z: float


def w2s(pos: Vec3, matrix):
    z = pos.x * matrix[12] + pos.y * matrix[13] + pos.z * matrix[14] + matrix[15]
    if z < 0.1:
        return None

    x = pos.x * matrix[0] + pos.y * matrix[1] + pos.z * matrix[2] + matrix[3]
    y = pos.x * matrix[4] + pos.y * matrix[5] + pos.z * matrix[6] + matrix[7]

    xx = x / z
    yy = y / z

    _x = (1920 / 2 * xx) + (xx + 1920 / 2)
    _y = (1090 / 2 * yy) + (yy + 1080 / 2)

    return [_x, _y]
