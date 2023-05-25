from pyglet.window import mouse
from vec2py.entities.Entity import Entity
from vec2py.util.Vector import Vector

class Events:
    def __init__(self):
        self.drag_object = None # Référence à l'objet que l'on déplace
        self.cue_object = None # Référence à l'objet qui va être tiré

        self.last_speeds = [Vector(0, 0)] * 10
        self.cursorpos = Vector(0, 0)
        self.target = None # Référence à l'objet selectionné pour les informations

    # FIRST HIT
    def on_mouse_press(self, x, y, button, modifiers):
        self.cursorpos = Vector(x, y)
        if button in (mouse.LEFT, mouse.RIGHT):
            for _ in Entity.get_movables():
                if _.is_inside(self.cursorpos) and _.maneuverable:
                    
                    if (button == mouse.LEFT) and self.drag_object is None: # Drag
                        _.full_stop()
                        self.target = _
                        self.drag_object = _

                    elif (button == mouse.RIGHT) and self.cue_object is None: # Cue
                        self.target = _
                        self.cue_object = _

    # WHILE
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if (buttons & mouse.LEFT) and self.drag_object is not None:
            self.drag_object.x += dx
            self.drag_object.y += dy
            self.last_speeds.pop(0)
            self.last_speeds.append(Vector(dx, dy)*600) # dépends BEAUCOUP de DT c'est chiant

        if (buttons & mouse.RIGHT) and self.cue_object is not None:
            self.cursorpos = Vector(x, y)
                
    # AFTER
    def on_mouse_release(self, x, y, button, modifiers):
        if (button & mouse.LEFT) and self.drag_object is not None:
            avg_x = sum(map(lambda _: _.getX(), self.last_speeds)) / len(self.last_speeds)
            avg_y = sum(map(lambda _: _.getY(), self.last_speeds)) / len(self.last_speeds)
            self.drag_object.internal_forces["A"] = Vector(avg_x, avg_y)

            self.drag_object = None
            self.last_speeds = [Vector(0, 0)] * 10

        elif (button & mouse.RIGHT) and self.cue_object is not None:
            self.cue_object.internal_forces["Q"] = Vector(self.cue_object.x - x, self.cue_object.y - y) * 5
            self.cue_object = None