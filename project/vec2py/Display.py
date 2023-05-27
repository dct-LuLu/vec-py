import os, sys, pyglet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyglet import shapes
from vec2py.Events import Events
from vec2py.entities import Circ, Rect
from vec2py.CollisionDetection import CollisionDetection, PolygonMapQuadtree
from vec2py.util import DoubleRect, Util, Vector2D
from vec2py.engine.maths.Solver import Solver
from vec2py.entities.Entity import Entity


class Display(Events, pyglet.window.Window):
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        pyglet.window.Window.__init__(self, width=window_width, height=window_height)
        if Util.DEBUG:
            self.quad_render = []

        self.solver = Solver()
        Events.__init__(self)
        # self.temp_render_list = [Circ(100, 100, 50, None, (98, 12, 225, 230)), Circ(200, 200, 13, None, (98, 12, 225, 230))]
        self.temp_render_list = [Rect(400, 300, 150, 100, 15), Rect(150, 250, 100, 25, 30)]

        pyglet.clock.schedule_interval(self.remake, 1 / 60.0)
        pyglet.clock.schedule_interval(self.simulate, 1 / 60)
        setting = "quadtree"
        setting = "SAT"
        self.collision_detection = CollisionDetection(self.window_width, self.window_height, setting)
        print(f"Collision detection set to {setting}")

        pyglet.app.run()

    def simulate(self, dt):
        self.solver.simulate(self, dt)

    def remake(self, dt):
        self.collision_detection.routine()
        if Util.DEBUG:
            if isinstance(self.collision_detection.system, PolygonMapQuadtree):
                self.quad_render = self.collision_detection.system.get_debug_lines()

            for i in CollisionDetection.may_collide:
                a = list(i)
                if len(a) == 2:
                    Entity.agagag_collision(self, *a)

                iterable = iter(i)

                string = "Collision between " + str(next(iterable))

                for _ in iterable:
                    string += " and " + str(_)

                print(string)

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