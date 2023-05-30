import os, sys, pyglet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyglet import shapes
from vec2py.Events import Events
from vec2py.entities import Circ, Rect
from vec2py.CollisionDetection import CollisionDetection, PolygonMapQuadtree, CollisionSAT
from vec2py.util import Util, Vector2D
from vec2py.engine.maths.Solver import Solver
from vec2py.entities.Entity import Entity
from vec2py.Menu import Menu
from vec2py.engine.maths.CollisionHandler import CollisionHandler
from random import randrange


class Display(Events, pyglet.window.Window, Menu):
    def __init__(self, window_width, window_height, collision_mode, solver_mode, handler_mode):
        self.window_width = window_width
        self.window_height = window_height
        pyglet.window.Window.__init__(self, window_width, window_height)

        Menu.__init__(self)
        Events.__init__(self)

        self.fps_counter = pyglet.window.FPSDisplay(window=self)
        self.cue_line = shapes.Line(0, 0, 0, 0, color = (255, 255, 255, 120), width=3)
        self.init_random_shapes()


        self.speed_force = 10
        self.default_solver = solver_mode
        self.solver = Solver(self.default_solver)

        self.default_handler = handler_mode
        self.collision_handler = CollisionHandler(self.default_handler)
        self.collision_detection = CollisionDetection(self.window_width, self.window_height, collision_mode)

        print(f"Current setup:\n\tSolver: {solver_mode}\n\tCollision Handler: {handler_mode}\n\tCollision Detection: {collision_mode}")
        #walls = [Rect(self.window_width / 2, 0, self.window_width, 30, is_static=True)]

        pyglet.clock.schedule_interval(self.remake, 1 / 240)
        pyglet.clock.schedule_interval(self.step, 1 / 240)
        pyglet.app.run()

    def init_random_shapes(self):
        rlist = []
        number_of_shapes = randrange(2, 10)
        for _ in range(number_of_shapes):
            type_of_shape = randrange(0, 2)
            velocity_x = randrange(-50, 50)
            velocity_y = randrange(-50, 50)
            angular_velocity = randrange(-15, 15)
            color = (randrange(0, 255), randrange(0, 255), randrange(0, 255), randrange(60, 255))
            match type_of_shape:
                case 0:
                    width = randrange(10, 100)
                    height = randrange(10, 100)
                    x = randrange(width, self.window_width-width)
                    y = randrange(height, self.window_height-height)
                    rotation = randrange(0, 360)
                    shape = Rect(x, y, width, height, rotation, color, False, True, 0.388, velocity_x, velocity_y, angular_velocity)
                case 1:
                    radius = randrange(5, 50)
                    x = randrange(radius, self.window_width-radius)
                    y = randrange(radius, self.window_height-radius)
                    shape = Circ(x, y, radius, None, 0, (98, 12, 225, 230), False, True, 0.388, velocity_x, velocity_y, angular_velocity)
                case 2:
                    pass
                case _:
                    raise Exception("Invalid shape type")
            rlist.append(shape)
        return rlist



    def step(self, dt):
        dt *= self.speed_force
        self.solver.step(self, dt)

    def remake(self, dt=None):
        self.collision_detection.routine()
        for polygons in Util.unique_sets(set(Entity.get_entities())):
            result = CollisionSAT.collision_check_SAT(*polygons)
            if result[0]:
                self.collision_handler.handle(polygons, result[1], result[2])


    def on_draw(self):
        self.clear()

        self.cue_line_update()
        self.cue_line.draw()
        
        self.menu_draw()

        if Util.DEBUG:
            self.fps_counter.draw()
            if isinstance(self.collision_detection.system, PolygonMapQuadtree):
                for i in PolygonMapQuadtree.debug_squares:
                    i.draw()
                for i in PolygonMapQuadtree.debug_lines:
                    i.draw()

            for i in Util.LINES:
                i.draw()
            Util.LINES = []

        for entities in Entity.get_entities():
            entities.draw()

def init_choices():
    print("Choose your window width (between 800 and 1900)")
    while True:
        width = input().strip()
        if width == "": # FAST SKIP
            width = 800
            break
        else:
            try:
                width = int(width)
                if width not in range(800, 1901):
                    print("Invalid input, retry again")
                else:
                    break
            except:
                print("Invalid input, retry again")

    print("\nChoose your window height (between 600 and 1000)")
    while True:
        height = input().strip()
        if height == "":
            height = 600
            break
        else:
            try:
                height = int(height)
                if height not in range(600, 1001):
                    print("Invalid input, retry again")
                else:
                    break
            except:
                print("Invalid input, retry again")


    print("Would you rather use Single Axis Theorem or a Quadtree? (SAT/quadtree)?")
    while True:
        collision_mode = input().strip()
        if collision_mode == "": # FAST SKIP
            collision_mode = "SAT"
            break
        elif collision_mode not in ("SAT", "quadtree"):
            print("Invalid input, retry again")
        else:
            break


    print("\nWould you rather use Euler or Verlet? (euler/verlet)?")
    while True:
        solver_mode = input().strip()
        if solver_mode == "": # FAST SKIP
            solver_mode = "euler"
            break
        elif solver_mode not in ("euler", "verlet"):
            print("Invalid input, retry again")
        else:
            break


    print("\nWould you rather use the ellastic, minimal, normal or full collision handler? (ellastic/minimal/normal/full)?")
    while True:
        handler_mode = input().strip()
        if handler_mode == "": # FAST SKIP
            handler_mode = "normal"
            break
        elif handler_mode not in ("ellastic", "minimal", "normal", "full"):
            print("Invalid input, retry again")
        else:
            break
    return width, height, collision_mode, solver_mode, handler_mode

if __name__ == "__main__":
    a = Display(*init_choices())

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