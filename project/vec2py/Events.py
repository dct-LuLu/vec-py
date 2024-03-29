from pyglet.window import mouse, key
from vec2py.entities.Entity import Entity
from vec2py.util.Vector2D import Vector2D
from vec2py.util.Util import Util
from vec2py.engine.maths.Solver import Solver
from vec2py.engine.maths.CollisionHandler import CollisionHandler

class Events:
    def __init__(self):
        self.drag_object = None  # Référence à l'objet que l'on déplace
        self.cue_object = None  # Référence à l'objet qui va être tiré

        self.last_speeds = [Vector2D(0, 0)] * 10
        self.cursor_pos = Vector2D(0, 0)
        self.target = None  # Référence à l'objet selectionné pour les informations

    # FIRST HIT
    def on_mouse_press(self, x, y, button, modifiers=None):
        self.cursor_pos = Vector2D(x, y)
        if button in (mouse.LEFT, mouse.RIGHT):
            for _ in Entity.get_movables():
                if _.contains(self.cursor_pos) and _.maneuverable:

                    if (button == mouse.LEFT) and self.drag_object is None:  # Drag
                        self.target = _
                        self.drag_object = _

                    elif (button == mouse.RIGHT) and self.cue_object is None:  # Cue
                        self.target = _
                        self.cue_object = _

    # WHILE
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers=None):
        if (buttons & mouse.LEFT) and self.drag_object is not None:
            self.drag_object.full_stop()
            self.drag_object.x += dx
            self.drag_object.y += dy
            self.last_speeds.pop(0)
            self.last_speeds.append(Vector2D(dx, dy) * 600)  # dépends BEAUCOUP de DT c'est chiant

        if (buttons & mouse.RIGHT) and self.cue_object is not None:
            self.cursor_pos = Vector2D(x, y)
                
    # AFTER
    def on_mouse_release(self, x, y, button, modifiers=None):
        if (button & mouse.LEFT) and self.drag_object is not None:
            avg_x = sum(map(lambda _: _.get_x(), self.last_speeds)) / len(self.last_speeds)
            avg_y = sum(map(lambda _: _.get_y(), self.last_speeds)) / len(self.last_speeds)
            self.drag_object.internal_forces["A"] = Vector2D(avg_x, avg_y)

            self.drag_object = None
            self.last_speeds = [Vector2D(0, 0)] * 10

        elif (button & mouse.RIGHT) and self.cue_object is not None:
            self.cue_object.internal_forces["Q"] = Vector2D(self.cue_object.x - x, self.cue_object.y - y) * 5
            self.cue_object = None

    def cue_line_update(self):
        """Dessine la ligne de visée"""
        if self.cue_object is not None:
            self.cue_line.x = self.cue_object.x
            self.cue_line.y = self.cue_object.y
            self.cue_line.x2 = self.cursor_pos.get_x()
            self.cue_line.y2 = self.cursor_pos.get_y()
            self.cue_line.visible = True
        else:
            self.cue_line.visible = False

    def on_key_press(self, symbol, modifiers=None):
        if symbol in (key.LCTRL, key.RCTRL):
            Util.DEBUG = not Util.DEBUG
            str = "ON" if Util.DEBUG else "OFF"
            print("\033cDEBUG MODE "+str)
        elif symbol == key.TAB:
            self.pannel_visible = not self.pannel_visible
        elif symbol in (key.LSHIFT,key.RSHIFT):
            if self.speed_force == 1:
                self.speed_force = 10
            else:
                self.speed_force = 1
        elif symbol == key.SPACE:
            if self.solver.setting != "ellastic":
                self.solver = Solver("ellastic")
                self.collision_handler = CollisionHandler("ellastic")
            else:
                self.solver = Solver(self.default_solver)
                self.collision_handler = CollisionHandler(self.default_handler)
        elif symbol == key.ENTER:
            #spawn shape
            pass