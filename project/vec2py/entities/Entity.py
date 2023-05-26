from vec2py.util import DoubleRect, Vector
from vec2py.engine.maths.Constants import Constants
import math

import inspect

class Entity:
    instances: set = set()

    def __init__(self, fixed=False, maneuverable=True, density=0.388, x_velocity=0, y_velocity=0, angular_velocity=0):
        self.fixed = fixed # Si l'entité est fixe (ne bouge pas)
        self.maneuverable = maneuverable # Si l'entité peut être contrôlée par le joueur

        self.density = density if not fixed else float('inf') # La densité de l'entité


        self.area = self.get_area() # L'aire de l'entité
        self.mass = self.get_mass() if not fixed else float('inf') # La masse de l'entité

        self.x_velocity = x_velocity if not fixed else 0

        self.y_velocity = y_velocity if not fixed else 0
    
        self.angular_velocity = angular_velocity
        self.angular_acceleration = 0

        self.internal_forces = {}
        self.external_forces = {}
        self._net_force = Vector(0, 0)        
        
        Entity.instances.add(self)

    def agagag_collision(self, b):
        # https://www.myphysicslab.com/engine2D/collision-en.html#resting_contact
        a = self

        P = "" # collision point
        ma, mb = a.mass, b.mass
        rap = Vector(P.getX() - a.x, P.getY() - a.y)
        rbp = Vector(P.getX() - b.x, P.getY() - b.y)
        wa1, wb1 = a.angular_velocity, b.angular_velocity
        wa2, wb2 = 0, 0

        va1, vb1 = 



    def collision(self, other):
        # Calcul des vitesses de collision
        relative_velocity_x = other.x_velocity - self.x_velocity
        relative_velocity_y = other.y_velocity - self.y_velocity

        # Calcul de l'angle d'impact
        collision_angle = math.atan2(other.y - self.y, other.x - self.x)

        # Calcul des vitesses tangentielles
        tangential_velocity1 = -self.angular_velocity * math.sin(collision_angle) * self.moment_of_inertia
        tangential_velocity2 = other.angular_velocity * math.sin(collision_angle) * other.moment_of_inertia

        # Calcul des vitesses normales
        normal_velocity1 = (relative_velocity_x * math.cos(collision_angle) +
                            relative_velocity_y * math.sin(collision_angle)) * self.mass
        normal_velocity2 = (relative_velocity_x * math.cos(collision_angle) +
                            relative_velocity_y * math.sin(collision_angle)) * other.mass

        # Calcul des nouvelles vitesses normales après collision
        new_normal_velocity1 = (normal_velocity1 * (self.mass - other.mass) +
                                2 * other.mass * normal_velocity2) / (self.mass + other.mass)
        new_normal_velocity2 = (normal_velocity2 * (other.mass - self.mass) +
                                2 * self.mass * normal_velocity1) / (self.mass + other.mass)

        # Calcul des nouvelles vitesses angulaires après collision
        self.angular_velocity = (self.angular_velocity * (self.moment_of_inertia - other.moment_of_inertia) +
                                2 * other.moment_of_inertia * other.angular_velocity) / (
                                        self.moment_of_inertia + other.moment_of_inertia)
        other.angular_velocity = (other.angular_velocity * (other.moment_of_inertia - self.moment_of_inertia) +
                                2 * self.moment_of_inertia * self.angular_velocity) / (
                                        self.moment_of_inertia + other.moment_of_inertia)

        # Mise à jour des vitesses des objets après collision

        vx1 = (new_normal_velocity1 * math.cos(collision_angle) -
                            tangential_velocity1 * math.sin(collision_angle)) / self.mass
        vy1 = (new_normal_velocity1 * math.sin(collision_angle) +
                            tangential_velocity1 * math.cos(collision_angle)) / self.mass

        vx2 = (new_normal_velocity2 * math.cos(collision_angle) -
                            tangential_velocity2 * math.sin(collision_angle)) / other.mass
        vy2 = (new_normal_velocity2 * math.sin(collision_angle) +
                            tangential_velocity2 * math.cos(collision_angle)) / other.mass

        self.external_forces['C'] = Vector(vx1, vy1)
        other.external_forces['C'] = Vector(vx2, vy2)



    def apply_net_forces(self):
        #print(f"F {sum(self.internal_forces.values())} , A{sum(self.external_forces.values())}")
        self._net_force = Vector(0, 0)
        self._net_force = sum(self.internal_forces.values()) + sum(self.external_forces.values())
        self.internal_forces = {}
        self.external_forces = {}

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
