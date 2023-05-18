import os, sys, pyglet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyglet import shapes
from vec2py.Events import Events
from vec2py.entities.Circ import Circ
from vec2py.CollisionDetection import CollisionDetection



class Display(Events, pyglet.window.Window):
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        pyglet.window.Window.__init__(self, width=window_width, height=window_height)
        self.quad_render = []
        
        Events.__init__(self)
        self.temp_render_list = [Circ(100, 100, 50, None, (98, 12, 225, 230)), Circ(200, 200, 13, None, (98, 12, 225, 230))]
        #pyglet.clock.schedule_interval(self.grow, 1/40)
        pyglet.clock.schedule_interval(self.remake, 1)
        self.collision_detection = CollisionDetection(self.window_width, self.window_height)
        pyglet.app.run()

    def remake(self, dt):
        print("remake")
        self.collision_detection.routine()
        self.quad_render = self.collision_detection.get_debug_lines()

    def on_draw(self):
        self.clear()
        for i in self.quad_render: i.draw()
        for i in self.temp_render_list: i.draw()

    def grow(self, dt):
        self.temp_render_list[0].radius += 1
        print(self.temp_render_list[0].get_pos())
        print(self.temp_render_list[0].get_AABB())
        


if __name__ == "__main__":
    a = Display(800, 600)
