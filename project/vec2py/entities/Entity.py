from vec2py.util import DoubleRect, Vector2D
from vec2py.engine.maths.Constants import Constants
from vec2py.util import Util
import math

import inspect


class Entity:
    instances: set = set()

    def __init__(self, is_static=False, maneuverable=True, density=0.388, x_velocity=0, y_velocity=0, angular_velocity=0):
        self.is_static = is_static  # Si l'entité est fixe (ne bouge pas)
        self.maneuverable = maneuverable  # Si l'entité peut être contrôlée par le joueur

        self.density = density if not is_static else float('inf')  # La densité de l'entité

        self.area = self.get_area()  # L'aire de l'entité
        self.mass = self.get_mass() if not is_static else float('inf')  # La masse de l'entité
        self.inv_mass = 1 / self.mass

        self.inertia = 0.7
        self.inv_inertia = 1 / self.inertia if self.inertia > 0 else 0

        self.x_velocity = x_velocity if not is_static else 0

        self.y_velocity = y_velocity if not is_static else 0

        self.angular_velocity = angular_velocity
        self.angular_acceleration = 0

        self.internal_forces = {}
        self.external_forces = {}
        self._net_force = Vector2D(0, 0)

        self.restitution = 0.9
        self.static_friction = 0.6
        self.dynamic_friction = 0.4

        Entity.instances.add(self)

    def apply_net_forces(self):
        self._net_force = Vector2D(0, 0)
        self._net_force = sum(self.internal_forces.values()) + sum(self.external_forces.values())
        self.internal_forces = {}
        self.external_forces = {}

    def get_velocity(self) -> Vector2D:
        return Vector2D(self.x_velocity, self.y_velocity)

    def set_velocity(self, vector: Vector2D) -> None:
        self.x_velocity = vector.get_x()
        self.y_velocity = vector.get_y()

    def add_velocity(self, vector: Vector2D) -> None:
        self.x_velocity += vector.get_x()
        self.y_velocity += vector.get_y()

    def full_stop(self):
        self.internal_forces = {}
        self.external_forces = {}
        self._net_force = Vector2D(0, 0)
        self.x_velocity = 0
        self.y_velocity = 0
        self.angular_velocity = 0

    @classmethod
    def get_entities(cls):
        return cls.instances

    @classmethod
    def get_movables(cls):
        return [entity for entity in cls.instances if not entity.is_static]

    def get_pos(self):
        """
        Returns the position of the circle as a Vector
        """
        return Vector2D(self.x, self.y)

    def move(self, vector: Vector2D):
        self.x += vector.get_x()
        self.y += vector.get_y()

    def get_AABB(self) -> DoubleRect:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_axes_SAT(self) -> list[Vector2D]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_corners(self) -> tuple[Vector2D, Vector2D]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def project_shape_onto_axis(self, axis: Vector2D) -> "Projection":
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    class Projection:
        def __init__(self, min: float, max: float):
            self.min = min
            self.max = max

        def overlap(self, other: "Entity.Projection"):
            return self.min < other.max and other.min < self.max

        def get_overlap(self, other: "Entity.Projection"):
            return min(self.max, other.max) - max(self.min, other.min)

        def get_axis_depth(self, other: "Entity.Projection") -> float:
            return min(other.max - self.min, self.max - other.min)
