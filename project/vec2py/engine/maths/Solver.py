from vec2py.engine.Walls import Walls
from vec2py.engine.maths.Constants import Constants
from vec2py.util import Vector2D


class Solver:
    def __init__(self, setting="euler"):
        match setting:
            case "euler":
                self.solver = SemiImplicitEuler
            case "verlet":
                self.solver = Verlet
            case _:
                raise Exception("Invalid solver setting")

    def step(self, sup, dt):
        for shape in sup.temp_render_list:
            if shape != sup.drag_object:
                if not shape.is_static:
                    Walls.check(sup, shape)
                    self.solver.step(shape, dt)


class SemiImplicitEuler:
    @staticmethod
    def step(shape, dt):
        shape.internal_forces["G"] = Constants.GRAVITY
        shape.internal_forces["r"] = Vector2D(shape.x_velocity,
                                              shape.y_velocity) * -shape.air_resistance_coefficient * dt
        shape.apply_net_forces()

        # Mise à jour des vélocitées
        shape.x_velocity += shape._net_force.get_x() * dt
        shape.y_velocity += shape._net_force.get_y() * dt
        shape.angular_velocity += shape.angular_acceleration * dt

        # Mise à jour des positions
        shape.x += shape.x_velocity * dt
        shape.y += shape.y_velocity * dt
        shape.rotation += shape.angular_velocity * dt


class Verlet:
    @staticmethod
    def step(shape, dt):
        # Calcul des forces internes
        shape.internal_forces["G"] = Constants.GRAVITY
        shape.internal_forces["r"] = Vector2D(shape.x_velocity,
                                              shape.y_velocity) * -shape.air_resistance_coefficient * dt
        shape.apply_net_forces()

        # Mise à jour de la position
        shape.x += shape.x_velocity * dt + 0.5 * shape._net_force.get_x() * dt * dt / shape.mass
        shape.y += shape.y_velocity * dt + 0.5 * shape._net_force.get_y() * dt * dt / shape.mass

        # Calcul des nouvelles forces internes
        new_internal_forces = {"G": Constants.GRAVITY * shape.mass, "r": Vector2D(shape.x_velocity,
                                                                                  shape.y_velocity) * -shape.air_resistance_coefficient * dt}
        shape.internal_forces = new_internal_forces

        # Mise à jour de la vitesse
        shape.x_velocity += 0.5 * (shape._net_force.get_x() + shape.internal_forces["r"].get_x()) * dt / shape.mass
        shape.y_velocity += 0.5 * (shape._net_force.get_y() + shape.internal_forces["r"].get_y()) * dt / shape.mass
        shape.angular_velocity += shape.angular_acceleration * dt

        # Mise à jour de la rotation
        shape.rotation += shape.angular_velocity * dt
