from vec2py.util.Vector2D import Vector2D
from vec2py.util.Util import Util
from vec2py.entities.Entity import Entity
from vec2py.entities.Circ import Circ
from vec2py.entities.Rect import Rect
from vec2py.engine.maths.Constants import Constants

class CollisionHandler:
    def __init__(self, setting):
        self.setting = setting
        match self.setting:
            case "ellastic":
                self.handler = EllasticHandler
            case "minimal":
                self.handler = MinimalHandler
            case "normal":
                self.handler = NormalHandler
            case "full":
                self.handler = FrictionHandler
            case _:
                raise Exception("Invalid collision handler setting")
    
    def handle(self, sup, a, b):
        self.handler.handle(sup, a, b)


    def separate_bodies(shape_a: Entity, shape_b: Entity, mtv: Vector2D):
        if shape_a.is_static:
            shape_b.move(mtv)
        elif shape_b.is_static:
            shape_a.move(mtv * -1)
        else:
            shape_a.move(mtv / 2 * -1)
            shape_b.move(mtv / 2)

    def find_contact_points(shape_a: Entity, shape_b: Entity):
        contact1 = Vector2D(0, 0)
        contact2 = Vector2D(0, 0)
        contactCount = 0

        if (type(shape_a) == Rect):
            if (type(shape_b) == Rect):
                contact1, contact2, contactCount = CollisionHandler.find_polygons_contact_points(shape_a.get_corners(), shape_b.get_corners())
            else:
                contact1 = CollisionHandler.find_circle_polygon_contact_point(shape_b.get_pos(), shape_a.get_corners())
                contactCount = 1
        else:
            if (type(shape_b) == Rect):
                contact1 = CollisionHandler.find_circle_polygon_contact_point(shape_a.get_pos(), shape_b.get_corners())
                contactCount = 1
            else:
                contact1 = CollisionHandler.find_circles_contact_point(shape_a.get_pos(), shape_a.radius, shape_b.get_pos())
                contactCount = 1

        return contact1, contact2, contactCount

    def find_polygons_contact_points(vertices_a: list[Vector2D], vertices_b: list[Vector2D]) -> tuple[Vector2D, Vector2D, float]:
        contact1 = Vector2D(0, 0)
        contact2 = Vector2D(0, 0)
        contactCount = 0

        minDistSq = float('inf')

        for i in range(len(vertices_a)):
            p = vertices_a[i]

            for j in range(len(vertices_b)):
                va = vertices_b[j]
                vb = vertices_b[(j + 1) % len(vertices_b)]

                distSq, cp = CollisionHandler.point_segment_distance(p, va, vb)

                if Util.near_equal(distSq, minDistSq, Constants.VERY_SMALL_AMOUNT):
                    if not Vector2D.near_equal(cp, contact1, Constants.VERY_SMALL_AMOUNT):
                        contact2 = cp
                        contactCount = 2
                elif distSq < minDistSq:
                    minDistSq = distSq
                    contactCount = 1
                    contact1 = cp

        for i in range(len(vertices_b)):
            p = vertices_b[i]

            for j in range(len(vertices_a)):
                va = vertices_a[j]
                vb = vertices_a[(j + 1) % len(vertices_a)]

                distSq, cp = CollisionHandler.point_segment_distance(p, va, vb)

                if Util.near_equal(distSq, minDistSq, Constants.VERY_SMALL_AMOUNT):
                    if not Vector2D.near_equal(cp, contact1, Constants.VERY_SMALL_AMOUNT):
                        contact2 = cp
                        contactCount = 2
                elif (distSq < minDistSq):
                    minDistSq = distSq
                    contactCount = 1
                    contact1 = cp

        return contact1, contact2, contactCount

    def find_circle_polygon_contact_point(circleCenter: Vector2D, polygonVertices: list[Vector2D]) -> Vector2D:
        cp = Vector2D(0, 0)

        minDistSq = float('inf')

        for i in range(len(polygonVertices)):
            va = polygonVertices[i]
            vb = polygonVertices[(i + 1) % len(polygonVertices)]

            distSq, contact = CollisionHandler.point_segment_distance(circleCenter, va, vb)

            if distSq < minDistSq:
                minDistSq = distSq
                cp = contact

        return cp

    def find_circles_contact_point(centerA: Vector2D, radiusA: float, centerB: Vector2D):
        ab = centerB - centerA
        cp = centerA + ab.normalize() * radiusA
        return cp

    def point_segment_distance(p: Vector2D, a: Vector2D, b: Vector2D):
        ab = b - a
        ap = p - a

        proj = Vector2D.dot_product(ap, ab)
        abLenSq = Vector2D.get_norm_squared(ab)
        d = proj / abLenSq

        if d <= 0:
            cp = a
        elif d >= 1:
            cp = b
        else:
            cp = a + ab * d

        distanceSquared = Vector2D.distance_squared(p, cp)
        return distanceSquared, cp



class EllasticHandler:
    @staticmethod
    def handle(sup, a, b):
        pass

class MinimalHandler:
    @staticmethod
    def handle(sup, a, b):
        pass

    def resolve_collisions_basic(self, shape_a: Entity, shape_b: Entity, normal: Vector2D):
        relativeVelocity = shape_b.get_velocity() - shape_a.get_velocity()

        if Vector2D.dot_product(relativeVelocity, normal) > 0:
            return

        e = min(shape_a.restitution, shape_b.restitution)

        j = -(1 + e) * Vector2D.dot_product(relativeVelocity, normal)
        j /= shape_a.inv_mass + shape_b.inv_mass

        impulse = j * normal

        shape_a.add_velocity(impulse * -shape_a.inv_mass)
        shape_b.add_velocity(impulse * shape_b.inv_mass)


class NormalHandler:
    @staticmethod
    def handle(polygons, normal=None, depth=None):
        CollisionHandler.separate_bodies(*polygons, normal * depth)
        contact1, contact2, contactCount = CollisionHandler.find_contact_points(*polygons)
        NormalHandler.resolve_collisions_with_rotation(*polygons, normal, contact1, contact2, contactCount)

    @staticmethod
    def resolve_collisions_with_rotation(shape_a: Entity, shape_b: Entity, normal: Vector2D, contact1: Vector2D, contact2: Vector2D, contactCount: int):
        e = min(shape_a.restitution, shape_b.restitution)

        contactList = [contact1, contact2]

        impulseList = [Vector2D(0, 0), Vector2D(0, 0)]
        raList = [Vector2D(0, 0), Vector2D(0, 0)]
        rbList = [Vector2D(0, 0), Vector2D(0, 0)]

        for i in range(contactCount):
            ra = contactList[i] - shape_a.get_pos()
            rb = contactList[i] - shape_b.get_pos()

            raList[i] = ra
            rbList[i] = rb

            raPerp = Vector2D(-ra.get_y(), ra.get_x())
            rbPerp = Vector2D(-rb.get_y(), rb.get_x())

            angularLinearVelocityA = raPerp * shape_a.angular_velocity
            angularLinearVelocityB = rbPerp * shape_b.angular_velocity

            relativeVelocity = (shape_b.get_velocity() + angularLinearVelocityB) - (shape_a.get_velocity() + angularLinearVelocityA)

            contactVelocityMag = Vector2D.dot_product(relativeVelocity, normal)

            if contactVelocityMag > 0:
                continue

            raPerpDotN = Vector2D.dot_product(raPerp, normal)
            rbPerpDotN = Vector2D.dot_product(rbPerp, normal)

            denom = shape_a.inv_mass + shape_b.inv_mass + (raPerpDotN * raPerpDotN) * shape_a.inv_inertia + (rbPerpDotN * rbPerpDotN) * shape_b.inv_inertia

            j = -(1 + e) * contactVelocityMag
            j /= denom
            j /= contactCount

            impulse = j * normal
            impulseList[i] = impulse

        for i in range(contactCount):
            impulse = impulseList[i]
            ra = raList[i]
            rb = rbList[i]

            shape_a.add_velocity(impulse * -shape_a.inv_mass)
            shape_a.angular_velocity = Vector2D.cross_product_2D(ra, impulse) * shape_a.inv_inertia
            shape_b.add_velocity(impulse * shape_b.inv_mass)
            shape_b.angular_velocity = -Vector2D.cross_product_2D(rb, impulse) * shape_b.inv_inertia


class FrictionHandler:
    @staticmethod
    def handle(sup, a, b):
        pass