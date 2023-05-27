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

    def simulate(self, sup, dt):
       
        # c'est de pire en pire va savoir pk tout pue la chiasse avec le dt je vais me pendre
        force = 10
        dt *= force

        for shape in sup.temp_render_list:
            if shape != sup.drag_object:
                self.solver.simulate(shape, dt)
                Walls.check(sup, shape)



class SemiImplicitEuler:
    @staticmethod
    def simulate(shape, dt):
        shape.internal_forces["G"] = Constants.GRAVITY * shape.mass
        shape.internal_forces["r"] = Vector2D(shape.x_velocity, shape.y_velocity) * -shape.air_resistance_coefficient * dt
        shape.apply_net_forces()

        # Mise à jour des vélocitées
        shape.x_velocity += shape._net_force.getX() * dt
        shape.y_velocity += shape._net_force.getY() * dt
        shape.angular_velocity += shape.angular_acceleration * dt

        # Mise à jour des positions
        shape.x += shape.x_velocity * dt
        shape.y += shape.y_velocity * dt
        shape.rotation += shape.angular_velocity * dt


class Verlet:
    @staticmethod
    def simulate(shape, dt):
        # Calcul des forces internes
        shape.internal_forces["G"] = Constants.GRAVITY * shape.mass
        shape.internal_forces["r"] = Vector2D(shape.x_velocity, shape.y_velocity) * -shape.air_resistance_coefficient * dt
        shape.apply_net_forces()

        # Mise à jour de la position
        shape.x += shape.x_velocity * dt + 0.5 * shape._net_force.getX() * dt * dt / shape.mass
        shape.y += shape.y_velocity * dt + 0.5 * shape._net_force.getY() * dt * dt / shape.mass

        # Calcul des nouvelles forces internes
        new_internal_forces = {}
        new_internal_forces["G"] = Constants.GRAVITY * shape.mass
        new_internal_forces["r"] = Vector2D(shape.x_velocity, shape.y_velocity) * -shape.air_resistance_coefficient * dt
        shape.internal_forces = new_internal_forces

        # Mise à jour de la vitesse
        shape.x_velocity += 0.5 * (shape._net_force.getX() + shape.internal_forces["r"].getX()) * dt / shape.mass
        shape.y_velocity += 0.5 * (shape._net_force.getY() + shape.internal_forces["r"].getY()) * dt / shape.mass
        shape.angular_velocity += shape.angular_acceleration * dt

        # Mise à jour de la rotation
        shape.rotation += shape.angular_velocity * dt





# RK-4 method python program

# function to be solved
def f(x,y):
    return x+y

# or
# f = lambda x: x+y

# RK-4 method
def rk4(x0,y0,xn,n):
    
    # Calculating step size
    h = (xn-x0)/n
    
    print('\n--------SOLUTION--------')
    print('-------------------------')    
    print('x0\ty0\tyn')
    print('-------------------------')
    for i in range(n):
        k1 = h * (f(x0, y0))
        k2 = h * (f((x0+h/2), (y0+k1/2)))
        k3 = h * (f((x0+h/2), (y0+k2/2)))
        k4 = h * (f((x0+h), (y0+k3)))
        k = (k1+2*k2+2*k3+k4)/6
        yn = y0 + k
        print('%.4f\t%.4f\t%.4f'% (x0,y0,yn) )
        print('-------------------------')
        y0 = yn
        x0 = x0+h
    
    print('\nAt x=%.4f, y=%.4f' %(xn,yn))

if __name__ == "__main__":
    # Inputs
    print('Enter initial conditions:')
    x0 = float(input('x0 = '))
    y0 = float(input('y0 = '))

    print('Enter calculation point: ')
    xn = float(input('xn = '))

    print('Enter number of steps:')
    step = int(input('Number of steps = '))

    # RK4 method call
    rk4(x0,y0,xn,step)