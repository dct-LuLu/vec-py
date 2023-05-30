from vec2py.entities.Entity import Entity
from pyglet import shapes
import math

class Poly(Entity, shapes.Polygon):
    def __init__(self, x, y, sides, siz, rotation=0, color=(255, 255, 255, 255), is_static=False, maneuverable=True, density=0.388, x_velocity=0, y_velocity=0, angular_velocity=0):
        self.s = sides
        self.siz = siz
        points = self.calculate_coordinates()
        shapes.Polygon.__init__(self, points, color)
        self.anchor_position = (0, 0)
        Entity.__init__(self, is_static, maneuverable, density, x_velocity, y_velocity, angular_velocity)

    def calculate_coordinates(self):
        coordinates = []
        angle = 360 / self.s  # Angle between each vertex of the pentagon

        for i in range(self.s):
            x = self.siz * math.cos(math.radians(i * angle))
            y = self.siz * math.sin(math.radians(i * angle))
            coordinates.append((x, y))

        return coordinates
    

if __name__ == "__main__":
    Poly(0, 0, 10, 10, (255, 255, 255, 255), False, True, 0.388, 0, 0, 0)