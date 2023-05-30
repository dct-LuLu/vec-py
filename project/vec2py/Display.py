import os, sys, pyglet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyglet import shapes
from vec2py.Events import Events
from vec2py.entities import Circ, Rect
from vec2py.CollisionDetection import CollisionDetection, PolygonMapQuadtree, CollisionSAT
from vec2py.util import DoubleRect, Util, Vector2D
from vec2py.engine.maths.Solver import Solver
from vec2py.entities.Entity import Entity


class Display(Events, pyglet.window.Window):
    VERY_SMALL_AMOUNT = 0.0005
    
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        pyglet.window.Window.__init__(self, width=window_width, height=window_height)
        if Util.DEBUG:
            self.quad_render = []

        self.solver = Solver("euler")
        Events.__init__(self)
        # self.temp_render_list = [Circ(100, 100, 50, color=(98, 12, 225, 230)), Circ(250, 250, 13, color=(98, 12, 225, 230))]
        walls = [Rect(self.window_width / 2, 0, self.window_width, 30, is_static=True)]
        self.temp_render_list = [Rect(400, 300, 150, 100, 15), Rect(150, 250, 100, 25, 30), Circ(100, 100, 50, None, 0, color=(98, 12, 225, 230)), Circ(50, 100, 50, None, 0, color=(98, 12, 225, 230))] + walls

        self.contactList = [0, 0]
        self.impulseList = [0, 0]
        self.raList = [0, 0]
        self.rbList = [0, 0]
        self.frictionImpulseList = [0, 0]
        self.jList = [0, 0]

        pyglet.clock.schedule_interval(self.remake, 1 / 120)
        pyglet.clock.schedule_interval(self.step, 1 / 120)
        setting = "quadtree"
        setting = "SAT"
        self.collision_detection = CollisionDetection(self.window_width, self.window_height, setting)
        print(f"Collision detection set to {setting}")

        pyglet.app.run()

    def step(self, dt):
        self.solver.step(self, dt)

    def remake(self, dt=None):
        for polygons in Util.unique_sets(set(Entity.get_entities())):
            result = CollisionSAT.collision_check_SAT(*polygons)

            if result[0]:
                normal, depth = result[1], result[2]

                Display.separate_bodies(*polygons, normal * depth);
                contact1, contact2, contactCount = Display.find_contact_points(*polygons)
                self.resolve_collisions_with_rotation(*polygons, normal, depth, contact1, contact2, contactCount)

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
                contact1, contact2, contactCount = Display.find_polygons_contact_points(shape_a.get_corners(), shape_b.get_corners())
            else:
                contact1 = Display.find_circle_polygon_contact_point(shape_b.get_pos(), shape_a.get_corners())
                contactCount = 1
        else:
            if (type(shape_b) == Rect):
                contact1 = Display.find_circle_polygon_contact_point(shape_a.get_pos(), shape_b.get_corners())
                contactCount = 1
            else:
                contact1 = Display.find_circles_contact_point(shape_a.get_pos(), shape_a.radius, shape_b.get_pos())
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

                distSq, cp = Display.PointSegmentDistance(p, va, vb)

                if Util.near_equal(distSq, minDistSq, Display.VERY_SMALL_AMOUNT):
                    if not Vector2D.near_equal(cp, contact1, Display.VERY_SMALL_AMOUNT):
                        contact2 = cp
                        contactCount = 2
                elif distSq < minDistSq:
                    minDistSq = distSq
                    contactCount = 1
                    contact1 = cp

        for i in range(len(vertices_b)):
            p = vertices_b[i]

            for j in range(len(vertices_a)):
                va = vertices_a[j];
                vb = vertices_a[(j + 1) % len(vertices_a)];

                distSq, cp = Display.PointSegmentDistance(p, va, vb)

                if Util.near_equal(distSq, minDistSq, Display.VERY_SMALL_AMOUNT):
                    if not Vector2D.near_equal(cp, contact1, Display.VERY_SMALL_AMOUNT):
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
            va = polygonVertices[i];
            vb = polygonVertices[(i + 1) % len(polygonVertices)];

            distSq, contact = Display.PointSegmentDistance(circleCenter, va, vb);

            if distSq < minDistSq:
                minDistSq = distSq;
                cp = contact

        return cp

    def find_circles_contact_point(centerA: Vector2D, radiusA: float, centerB: Vector2D):
        ab = centerB - centerA
        cp = centerA + ab.normalize() * radiusA
        return cp

    def PointSegmentDistance(p: Vector2D, a: Vector2D, b: Vector2D):
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

    def resolve_collisions_basic(self, shape_a: Entity, shape_b: Entity, normal: Vector2D, depth: float, contact1: Vector2D, contact2: Vector2D, contactCount: int):
        relativeVelocity = shape_b.get_velocity() - shape_a.get_velocity();

        if Vector2D.dot_product(relativeVelocity, normal) > 0:
            return

        e = min(shape_a.restitution, shape_b.restitution)

        j = -(1 + e) * Vector2D.dot_product(relativeVelocity, normal)
        j /= shape_a.inv_mass + shape_b.inv_mass

        impulse = j * normal

        shape_a.add_velocity(impulse * -shape_a.inv_mass)
        shape_b.add_velocity(impulse * shape_b.inv_mass)

    def resolve_collisions_with_rotation(self, shape_a: Entity, shape_b: Entity, normal: Vector2D, depth: float, contact1: Vector2D, contact2: Vector2D, contactCount: int):
        e = min(shape_a.restitution, shape_b.restitution)

        self.contactList = [contact1, contact2]

        self.impulseList = [Vector2D(0, 0), Vector2D(0, 0)]
        self.raList = [Vector2D(0, 0), Vector2D(0, 0)]
        self.rbList = [Vector2D(0, 0), Vector2D(0, 0)]

        for i in range(contactCount):
            ra = self.contactList[i] - shape_a.get_pos()
            rb = self.contactList[i] - shape_b.get_pos()

            self.raList[i] = ra
            self.rbList[i] = rb

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
            self.impulseList[i] = impulse

        for i in range(contactCount):
            impulse = self.impulseList[i]
            ra = self.raList[i]
            rb = self.rbList[i]

            shape_a.add_velocity(impulse * -shape_a.inv_mass)
            shape_a.angular_velocity = Vector2D.cross_product_2D(ra, impulse) * shape_a.inv_inertia
            shape_b.add_velocity(impulse * shape_b.inv_mass)
            shape_b.angular_velocity = -Vector2D.cross_product_2D(rb, impulse) * shape_b.inv_inertia

    def on_draw(self):
        self.clear()

        if Util.DEBUG:
            if isinstance(self.collision_detection.system, PolygonMapQuadtree):
                for i in PolygonMapQuadtree.debug_squares:
                    i.draw()
                for i in self.quad_render:
                    i.draw()

        for i in self.temp_render_list:
            i.draw()

        for i in Util.LINES:
            i.draw()

        Util.LINES = []


if __name__ == "__main__":
    a = Display(800, 600)

# Designing a 2D physics engine involves simulating the physical behavior of objects in your virtual world.
# To compute the forces applied to each shape and determine their next positions,
# you can use a technique called rigid body simulation.

# Rigid body simulation typically involves solving a system of equations that describe the forces acting on the objects.
# These equations can be represented using matrices, and various numerical methods can be employed to solve these matrices and determine the object's motion.

# Here's a high-level overview of the process:

#   Define the physics properties of your objects: Each object should have attributes such as mass, position, velocity, and orientation.
#   You'll need to track these properties for each shape in your simulation.

#   Apply external forces: Start by applying any external forces acting on the objects, such as gravity or user-applied forces.
#   These forces can be computed based on the object's mass and the acceleration due to gravity.

#   Resolve collisions: Check for collisions between objects. If two objects intersect, you'll need to calculate the forces that arise from the collision.
#   There are various collision detection algorithms (e.g., bounding volume hierarchies, spatial partitioning) that can help identify colliding objects efficiently.

#   Compute internal forces: Calculate the internal forces within each object. These forces might arise from constraints 
#   (e.g., springs, joints) or object-specific behaviors (e.g., friction, elasticity).

#   Formulate equations of motion: Express the forces acting on each object as a set of equations of motion. These equations relate the object's
#   acceleration to the applied forces and can be written in matrix form.

#   Solve the equations using numerical methods: To determine the object's next position and velocity, you'll need to solve the system of equations
#   obtained in the previous step. Various numerical methods can be employed, such as the Euler method, Verlet integration, or more
#   sophisticated approaches like the Runge-Kutta method. These methods involve iterating over time steps to update the object's state
#   based on the computed forces.

# When solving the matrices, you may use techniques like matrix inversion, matrix multiplication, or
# decomposition methods (e.g., LU decomposition, Cholesky decomposition) to obtain the desired results.
# The choice of method depends on the specific requirements of your physics simulation.