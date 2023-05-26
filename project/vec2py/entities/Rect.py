from vec2py.entities.Entity import Entity
from vec2py.util import DoubleRect, Vector, Util
from math import pi, cos, sin, radians


from pyglet import shapes

class Rect(Entity, shapes.Rectangle):
    def __init__(self, x, y, width, height, rotation=0, color=(255, 255, 255, 255), fixed=False, maneuverable=True, density=0.388, x_velocity=0, y_velocity=0, angular_velocity=0):
        shapes.Rectangle.__init__(self, x, y, width, height, color)
        self.rotation = rotation
        self.anchor_position = (width / 2, height / 2)
        self.needUpdate = True
        self.air_resistance_coefficient = 1.05

        Entity.__init__(self, fixed, maneuverable, density, x_velocity, y_velocity, angular_velocity)

        self.moment_of_inertia = 1/12 * self.get_mass() * (self.width**2 + self.height**2)

    def get_area(self):
        return self.width/100 * self.height/100
    
    def get_mass(self):
        return self.area * self.density

    def draw(self):
        #self.rotation = (self.rotation + 1) % 360
        super().draw()
        self.needUpdate = True

    def get_corners(self) -> tuple[Vector, Vector, Vector, Vector]:
        r = radians(self.rotation)

        width = self.width / 2
        height = self.height / 2

        cosr = cos(r)
        sinr = -sin(r)

        a = Vector(self.x + (-width * cosr - -height * sinr), self.y + (-width * sinr + -height * cosr))
        b = Vector(self.x + (-width * cosr -  height * sinr), self.y + (-width * sinr +  height * cosr))
        c = Vector(self.x + ( width * cosr -  height * sinr), self.y + ( width * sinr +  height * cosr))
        d = Vector(self.x + ( width * cosr - -height * sinr), self.y + ( width * sinr + -height * cosr))

        return a, b, c, d

    def get_perfored_vector(self, p):
        a, b, c, _ = self.get_corners()
        if Util.is_point_on_segment(a, b, p):
            return a-b
        elif Util.is_point_on_segment(b, c, p):
            return b-c

    def get_min_max(self):
        a, b, c, d = self.get_corners()
        min_x = min(a.getX(), b.getX(), c.getX(), d.getX())
        min_y = min(a.getY(), b.getY(), c.getY(), d.getY())

        max_x = max(a.getX(), b.getX(), c.getX(), d.getX())
        max_y = max(a.getY(), b.getY(), c.getY(), d.getY())

        return Vector(min_x, min_y), Vector(max_x, max_y)

    def get_AABB(self):
        if self.needUpdate:
            self.aabb = self.get_min_max()
            self.needUpdate = False

        return DoubleRect.make(self.aabb[0], self.aabb[1])

    def get_pos(self):
        return Vector(self.x, self.y)

    def contains(self, point: Vector):
        return self.x - self.width / 2 <= point.getX() and self.x + self.width / 2 >= point.getX() \
            and self.y - self.height / 2 <= point.getY() and self.y + self.height / 2 >= point.getY()

    def is_point_inside(self, point, error_factor=1):
        # Translate the point and rectangle corners to the origin
        a, _, _, _ = self.get_corners()
        translated_point = Vector(point.getX() - a.getX(), point.getY() - a.getY())
        translated_corners = [
            Vector(corner.getX() - a.getX(), corner.getY() - a.getY())
            for corner in self.get_corners()
        ]

        # Rotate the point and rectangle corners by the negative of the rectangle's rotation angle
        rotated_point = Vector(
            translated_point.getX() * cos(-self.rotation) - translated_point.getY() * sin(-self.rotation),
            translated_point.getX() * sin(-self.rotation) + translated_point.getY() * cos(-self.rotation)
        )
        rotated_corners = [
            Vector(
                corner.getX() * cos(-self.rotation) - corner.getY() * sin(-self.rotation),
                corner.getX() * sin(-self.rotation) + corner.getY() * cos(-self.rotation)
            )
            for corner in translated_corners
        ]

        # Check if the rotated point is within the rectangle, considering the error factor
        min_x = min(corner.getX() for corner in rotated_corners)
        max_x = max(corner.getX() for corner in rotated_corners)
        min_y = min(corner.getY() for corner in rotated_corners)
        max_y = max(corner.getY() for corner in rotated_corners)

        if (
            rotated_point.getX() >= min_x - error_factor and
            rotated_point.getX() <= max_x + error_factor and
            rotated_point.getY() >= min_y - error_factor and
            rotated_point.getY() <= max_y + error_factor
        ):
            return True

        return False

    def get_axesSAT(self) -> list[Vector]:
        corners = self.get_corners()
        return [(corners[1] - corners[0]).getNormal().normalize(),
                (corners[2] - corners[1]).getNormal().normalize()]
    
    def __str__(self):
        return f"Rect(x={self.x}, y={self.y}, width={self.width}, height={self.height}, rotation={self.rotation})"
    
    def __repr__(self):
        return self.__str__()
