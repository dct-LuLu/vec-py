from vec2py.entities.Entity import Entity
from vec2py.util import DoubleRect, Vector2D, Util
from math import pi, cos, sin, radians

from pyglet import shapes


class Rect(Entity, shapes.Rectangle):
    def __init__(self, x, y, width, height, rotation=0, color=(255, 255, 255, 255), fixed=False, maneuverable=True,
                 density=0.388, x_velocity=0, y_velocity=0, angular_velocity=0):
        shapes.Rectangle.__init__(self, x, y, width, height, color)
        self.rotation = rotation
        self.anchor_position = (width / 2, height / 2)
        self.needUpdate = True
        self.air_resistance_coefficient = 1.05

        Entity.__init__(self, fixed, maneuverable, density, x_velocity, y_velocity, angular_velocity)

        self.moment_of_inertia = 1 / 12 * self.get_mass() * (self.width ** 2 + self.height ** 2)

    def get_area(self):
        return self.width / 100 * self.height / 100

    def get_mass(self):
        return self.area * self.density

    def draw(self):
        # self.rotation = (self.rotation + 1) % 360
        super().draw()
        self.needUpdate = True

    def get_corners(self) -> tuple[Vector2D, Vector2D, Vector2D, Vector2D]:
        r = radians(self.rotation)

        width = self.width / 2
        height = self.height / 2

        cosr = cos(r)
        sinr = -sin(r)

        a = Vector2D(self.x + (-width * cosr - -height * sinr), self.y + (-width * sinr + -height * cosr))
        b = Vector2D(self.x + (-width * cosr - height * sinr), self.y + (-width * sinr + height * cosr))
        c = Vector2D(self.x + (width * cosr - height * sinr), self.y + (width * sinr + height * cosr))
        d = Vector2D(self.x + (width * cosr - -height * sinr), self.y + (width * sinr + -height * cosr))

        return a, b, c, d

    def get_perfored_vector(self, p):
        a, b, c, d = self.get_corners()

        if Vector2D.is_point_on_segment(a, b, p):
            return a - b

        if Vector2D.is_point_on_segment(b, c, p):
            return b - c

        if Vector2D.is_point_on_segment(c, d, p):
            return c - d

        raise Exception('Unreachable code')

    def get_min_max(self):
        a, b, c, d = self.get_corners()
        min_x = min(a.get_x(), b.get_x(), c.get_x(), d.get_x())
        min_y = min(a.get_y(), b.get_y(), c.get_y(), d.get_y())

        max_x = max(a.get_x(), b.get_x(), c.get_x(), d.get_x())
        max_y = max(a.get_y(), b.get_y(), c.get_y(), d.get_y())

        return Vector2D(min_x, min_y), Vector2D(max_x, max_y)

    def get_AABB(self):
        if self.needUpdate:
            self.aabb = self.get_min_max()
            self.needUpdate = False

        return DoubleRect.make(self.aabb[0], self.aabb[1])

    def get_pos(self):
        return Vector2D(self.x, self.y)

    def contains(self, point: Vector2D):
        return self.x - self.width / 2 <= point.get_x() <= self.x + self.width / 2 \
            and self.y - self.height / 2 <= point.get_y() <= self.y + self.height / 2

    def is_point_inside(self, point, error_factor=1):
        # Translate the point and rectangle corners to the origin
        a, _, _, _ = self.get_corners()
        translated_point = Vector2D(point.get_x() - a.get_x(), point.get_y() - a.get_y())
        translated_corners = [
            Vector2D(corner.get_x() - a.get_x(), corner.get_y() - a.get_y())
            for corner in self.get_corners()
        ]

        # Rotate the point and rectangle corners by the negative of the rectangle's rotation angle
        rotated_point = Vector2D(
            translated_point.get_x() * cos(-self.rotation) - translated_point.get_y() * sin(-self.rotation),
            translated_point.get_x() * sin(-self.rotation) + translated_point.get_y() * cos(-self.rotation)
        )
        rotated_corners = [
            Vector2D(
                corner.get_x() * cos(-self.rotation) - corner.get_y() * sin(-self.rotation),
                corner.get_x() * sin(-self.rotation) + corner.get_y() * cos(-self.rotation)
            )
            for corner in translated_corners
        ]

        # Check if the rotated point is within the rectangle, considering the error factor
        min_x = min(corner.get_x() for corner in rotated_corners)
        max_x = max(corner.get_x() for corner in rotated_corners)
        min_y = min(corner.get_y() for corner in rotated_corners)
        max_y = max(corner.get_y() for corner in rotated_corners)

        if (
                min_x - error_factor <= rotated_point.get_x() <= max_x + error_factor and
                min_y - error_factor <= rotated_point.get_y() <= max_y + error_factor
        ):
            return True

        return False

    def get_axes_SAT(self) -> list[Vector2D]:
        corners = self.get_corners()
        return [(corners[1] - corners[0]).get_normal().normalize(),
                (corners[2] - corners[1]).get_normal().normalize()]

    def __str__(self):
        return f"Rect(x={self.x}, y={self.y}, width={self.width}, height={self.height}, rotation={self.rotation})"

    def __repr__(self):
        return self.__str__()
