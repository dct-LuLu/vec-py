class RungeKutta4:
    class State:
        def __init__(self, x, y, vx, vy):
            self.x = x      # position x
            self.y = y      # position y
            self.vx = vx    # velocity x
            self.vy = vy    # velocity y

    class Derivative:
        def __init__(self, dx, dy, dvx, dvy):
            self.dx = dx    # dx/dt = velocity x
            self.dy = dy    # dy/dt = velocity y
            self.dvx = dvx  # dvx/dt = acceleration x
            self.dvy = dvy  # dvy/dt = acceleration y

    def acceleration(state, t):
        # Compute acceleration in the x and y directions
        # based on the state of the object
        # Example: constant acceleration of -9.8 m/s^2 in the y direction (gravity)
        k = 15.0
        b = 0.1
        ax = 0.0
        ay = -9.8
        return -k * state.x - b * state.vx, -k * state.y - b * state.vy

    def evaluate(initial, t, dt, d):
        state = RungeKutta4.State(0, 0, 0, 0)
        state.x = initial.x + d.dx * dt
        state.y = initial.y + d.dy * dt
        state.vx = initial.vx + d.dvx * dt
        state.vy = initial.vy + d.dvy * dt

        output = RungeKutta4.Derivative(0, 0, 0, 0)
        output.dx = state.vx
        output.dy = state.vy
        output.dvx, output.dvy = RungeKutta4.acceleration(state, t + dt)
        return output

    def integrate(state, t, dt):
        a = RungeKutta4.evaluate(state, t, 0.0, RungeKutta4.Derivative(0, 0, 0, 0))
        b = RungeKutta4.evaluate(state, t, dt * 0.5, a)
        c = RungeKutta4.evaluate(state, t, dt * 0.5, b)
        d = RungeKutta4.evaluate(state, t, dt, c)

        dxdt = 1.0 / 6.0 * (a.dx + 2.0 * (b.dx + c.dx) + d.dx)
        dydt = 1.0 / 6.0 * (a.dy + 2.0 * (b.dy + c.dy) + d.dy)
        dvxdt = 1.0 / 6.0 * (a.dvx + 2.0 * (b.dvx + c.dvx) + d.dvx)
        dvydt = 1.0 / 6.0 * (a.dvy + 2.0 * (b.dvy + c.dvy) + d.dvy)

        state.x = state.x + dxdt * dt
        state.y = state.y + dydt * dt
        state.vx = state.vx + dvxdt * dt
        state.vy = state.vy + dvydt * dt
