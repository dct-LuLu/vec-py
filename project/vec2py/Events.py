from pyglet.window import mouse
from vec2py.entities.Entity import Entity
from vec2py.util.Vector import Vector

class Events:
    def __init__(self):
        self.drag_object = None # Référence à l'objet que l'on déplace
        self.cue_object = None # Référence à l'objet qui va être tiré

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

            self.drag_object.x_acceleration += (dx*10)
            self.drag_object.y_acceleration += (dy*10)

        if (buttons & mouse.RIGHT) and self.cue_object is not None:
            self.cursorpos = Vector(x, y)
                
    # AFTER
    def on_mouse_release(self, x, y, button, modifiers):
        if (button & mouse.LEFT) and self.drag_object is not None:
            self.drag_object = None

        elif (button & mouse.RIGHT) and self.cue_object is not None:
            self.cue_object.x_acceleration += (self.cue_object.x - x)*5
            self.cue_object.y_acceleration += (self.cue_object.y - y)*5
            self.cue_object = None