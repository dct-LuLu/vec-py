from vec2py.util import DoubleRect, Vector2D
from vec2py.engine.maths.Constants import Constants
from vec2py.util.Util import Util
from vec2py.util.Vector3D import Vector3D
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
        self._net_force = Vector2D(0, 0)        
        
        Entity.instances.add(self)

    

    @staticmethod
    def agagag_collision(a, b):
        # https://www.myphysicslab.com/engine2D/collision-en.html#resting_contact
        e = 0.8
        P, perf_obj = Entity.get_col(a, b)

        ma, mb = a.mass, b.mass

        rap = Vector2D(P.getX() - a.x, P.getY() - a.y)
        rbp = Vector2D(P.getX() - b.x, P.getY() - b.y)

        wa1, wb1 = a.angular_velocity, b.angular_velocity
        wa2, wb2 = None, None # WHAT WE WANT

        va1, vb1 = Vector2D(a.x_velocity, a.y_velocity), Vector2D(b.x_velocity, b.y_velocity)
        va2, vb2 = None, None # WHAT WE WANT

        n = perf_obj.get_perfored_vector(P).get_perpendicular_unit_vector()

        #####

        # relative my ass
        vap1 = va1 + rap.cross_product_sp(wa1)
        vbp1 = vb1 + rbp.cross_product_sp(wb1)
        #vap2 = va2 + rap.cross_product_sp(wa2)
        #vbp2 = vb2 + rbp.cross_product_sp(wb2)

        vab1 = vap1 - vbp1
        #vab2 = vap2 - vbp2

        rel_normal_velocity = vab1.dotProduct(n)

        # vab2.dotProduct(n) = -e * rel_normal_velocity

        if mb == float('inf'):
            j = (-(i+e)*vap1.dotProduct(n)) / (1/ma + (rap.cross_product_sp(n)**2/a.moment_of_inertia))
        elif ma == float('inf'):
            j = ((i+e)*vbp1.dotProduct(n)) / (1/mb + (rbp.cross_product_sp(n)**2/b.moment_of_inertia))
        else:
            j = (-(1+e)*rel_normal_velocity) / (1/ma + 1/mb + Vector3D.cross_product_2D(rap, n).self_dot_product()/a.moment_of_inertia
                + Vector3D.cross_product_2D(rbp, n).self_dot_product()/b.moment_of_inertia)

        va2 = va1 + j*n/ma
        vb2 = vb1 - j*n/mb

        wa2 = wa1 + Vector3D.cross_product_2D(rap, j*n).getZ()/a.moment_of_inertia
        wb2 = wb1 - Vector3D.cross_product_2D(rap, j*n).getZ()/b.moment_of_inertia

        a.x_velocity, a.y_velocity = va2.getX(), va2.getY()
        b.x_velocity, b.y_velocity = vb2.getX(), vb2.getY()

        a.angular_velocity = wa2
        b.angular_velocity = wb2

# to do after this works ^^^ https://www.myphysicslab.com/engine2D/collision-methods-en.html

    @staticmethod
    def get_col(a, b):
        for corner in a.get_corners():
            print(corner)
            if b.is_point_inside(corner):
                return corner, a
        print("----")
        for corner in b.get_corners():
            print(corner)
            if a.is_point_inside(corner):
                return corner, b
        raise Exception("No collision")

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

        self.external_forces['C'] = Vector2D(vx1, vy1)
        other.external_forces['C'] = Vector2D(vx2, vy2)



    def apply_net_forces(self):
        #print(f"F {sum(self.internal_forces.values())} , A{sum(self.external_forces.values())}")
        self._net_force = Vector2D(0, 0)
        self._net_force = sum(self.internal_forces.values()) + sum(self.external_forces.values())
        self.internal_forces = {}
        self.external_forces = {}

    def get_velocity(self) -> Vector2D:
        return Vector2D(self.x_velocity, self.y_velocity)

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

    def get_axesSAT(self) -> list[Vector2D]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')

    def get_corners(self) -> tuple[Vector2D, Vector2D]:
        raise Exception(f'{inspect.stack()[0][3]}() is not implemented for the class: {self.__class__} ')
