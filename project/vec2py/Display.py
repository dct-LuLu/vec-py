import os, sys, pyglet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyglet import shapes
from vec2py.Events import Events
from vec2py.entities.Circ import Circ
from vec2py.entities.Rect import Rect
from vec2py.CollisionDetection import CollisionDetection, CollisionSAT



class Display(Events, pyglet.window.Window):
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        pyglet.window.Window.__init__(self, width=window_width, height=window_height)
        self.quad_render = []
        
        Events.__init__(self)
        # self.temp_render_list = [Circ(100, 100, 50, None, (98, 12, 225, 230)), Circ(200, 200, 13, None, (98, 12, 225, 230))]
        self.temp_render_list = [Rect(400, 300, 150, 100, 15), Rect(150, 250, 100, 25, 30)]
        #pyglet.clock.schedule_interval(self.grow, 1/40)

        pyglet.clock.schedule_interval(self.remake, 1 / 60.0)
        #pyglet.clock.schedule_interval(self.simul, 1/600)
        self.collision_detection = CollisionDetection(self.window_width, self.window_height)
       
        pyglet.app.run()

    def simul(self, dt):
        dt *= 10
        force = 10
        for i in self.temp_render_list:
            if i != self.drag_object:
                i._x_velocity += i._x_acceleration * dt
                i._y_velocity += i._y_acceleration * dt

                i.x += i._x_velocity * dt
                i.y += i._y_velocity * dt

                #if i.x <= 0 or i.x >= self.window_width:
                    #i._x_velocity *= -1

                if i.y <= 0 or i.y >= self.window_height:
                    i._y_velocity *= -1

                if i.x < 0:
                    i.x = self.window_width-1

                if i.x > self.window_width:
                    i.x = 1

    def feur(self, dt):
        print(dt)

    def remake(self, dt):
        self.collision_detection.routine()
        self.quad_render = self.collision_detection.get_debug_lines()
        if len(CollisionDetection._may_collide) > 0:
            if CollisionSAT.collisionSAT(self.temp_render_list[0], self.temp_render_list[1]):
                print('collision')

    def on_draw(self):
        self.clear()
        for i in CollisionDetection._fun: i.draw()
        for i in self.quad_render: i.draw()
        for i in self.temp_render_list: i.draw()

    def grow(self, dt):
        self.temp_render_list[0].radius += 1
        print(self.temp_render_list[0].get_pos())
        print(self.temp_render_list[0].get_AABB())


if __name__ == "__main__":
    a = Display(800, 600)
