from vec2py.util import DoubleRect, Vector

import inspect

class Entity:
    instances: set = set()
    air_density =  1.2041 # kg/m^3

    def __init__(self, density, x_velocity=0, y_velocity=0, angular_velocity=5):
        self.density = density # La densité de l'entité
        self.area = self.get_area() # L'aire de l'entité
        self.mass = self.get_mass() # La masse de l'entité


        self.force = Vector(0, -9.8)# La force de l'entité
        self.x_velocity = x_velocity
        self.x_acceleration = 0 # L'accélération de l'entité

        self.y_velocity = y_velocity
        self.y_acceleration = (self.force.getY() / self.mass) # L'accélération de l'entité

        self.angular_velocity = angular_velocity # Jamais négatif et jamais supérieur à 360
        self.angular_acceleration = 0 # L'accélération angulaire de l'entité

        self.net_force = Vector(0, 0) # La force nette appliquée à l'entité

        self.fixed = False # Si l'entité est fixe (ne bouge pas)
        self.maneuverable = True # Si l'entité peut être contrôlée par le joueur
        Entity.instances.add(self)


    def get_air_resistance_force(self) -> Vector:
        a = self.air_resistance_coefficient 
        b = self.air_density
        c =((self.get_velocity()**2)/2)
        d = self.area #may need to use abs my ass
        return a*b*c*d

    def get_velocity(self) -> Vector:
        return Vector(self.x_velocity, self.y_velocity)

    def full_stop(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.angular_velocity = 0

    @classmethod
    def getEntities(cls):
        return cls.instances

    @classmethod
    def get_movables(cls):
        return [entity for entity in cls.instances if not entity.fixed]

    def get_AABB(self) -> DoubleRect:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_axesSAT(self) -> list[Vector]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_corners(self) -> tuple[Vector, Vector]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')
