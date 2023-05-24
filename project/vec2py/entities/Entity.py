from vec2py.util import DoubleRect, Vector

import inspect

class Entity:
    instances: set = set()
    air_density =  1.2041 # kg/m^3

    def __init__(self, x_velocity=0, y_velocity=0, angular_velocity=0):
        self._mass = 1 # La masse de l'entité
        force = -9.8# La force de l'entité
        self._x_velocity = x_velocity
        self._x_acceleration = 0 # L'accélération de l'entité

        self._y_velocity = y_velocity
        self._y_acceleration = (force / self._mass) # L'accélération de l'entité

        self._angular_velocity = angular_velocity # Jamais négatif et jamais supérieur à 360
        self._angular_acceleration = 0 # L'accélération angulaire de l'entité

        self._air_resistance_coefficient = 0.5

        self._net_force = Vector(0, 0) # La force nette appliquée à l'entité
        self.cross_sectional_area = 1

        self.fixed = False # Si l'entité est fixe (ne bouge pas)
        self.maneuverable = True # Si l'entité peut être contrôlée par le joueur
        Entity.instances.add(self)

    def get_accel(self) -> Vector:
        W = Vector(0, -9.8) * self._mass
        D = self.get_air_resistance_force()
        a = (W - D) / self._mass
        return a

    def get_air_resistance_force(self) -> Vector:
        Fd: Vector = self.Cd * self.air_density * ((self.get_velocity()**2)/2) * self.cross_sectional_area #may need to use abs my ass
        return Fd

    def apply_forces(self, *forces):
        for force in forces:
            self._net_force += force

    def get_velocity(self) -> Vector:
        return Vector(self._x_velocity, self._y_velocity)

    def full_stop(self):
        self._x_velocity = 0
        self._y_velocity = 0
        self._angular_velocity = 0

    @classmethod
    def getEntities(cls):
        return cls.instances

    @classmethod
    def get_movables(cls):
        return [entity for entity in cls.instances if not entity.fixed]

    @property
    def x_velocity(self):
        """The x velocity of the entity."""
        return self._x_velocity

    @x_velocity.setter
    def x_velocity(self, value):
        self._x_velocity = value

    def get_AABB(self) -> DoubleRect:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_axesSAT(self) -> list[Vector]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_corners(self) -> tuple[Vector, Vector]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')
