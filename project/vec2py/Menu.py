from pyglet import shapes, text

class Menu:
    def __init__(self):
        self.pannel_visible = False
        self.visible_pannel_shapes = self.init_visible_pannel()
        self.hidden_pannel_shapes = self.init_hidden_pannel()
        self.showcase_num = 2
        self.showcase_shape = None # Circle, Triangle, Square/Rectangle, Pentagon, Hexagon

    def init_visible_pannel(self):
        pannel = shapes.Rectangle(self.window_width / 8, self.window_height, self.window_width / 8*7, self.window_height / 8, color=(255, 255, 255, 255))

        return {name: value for name, value in vars().items() if name != "self"}
    
    def init_hidden_pannel(self):
        tooltip = text.Label("TAB: Show/Hide Menu", font_size=32, x=self.window_width / 8, y=self.window_height / 8, anchor_x="left", anchor_y="bottom", color=(0, 0, 0, 255))

        return {name: value for name, value in vars().items() if name != "self"}
    
    def change_showcase_to(self, num):
        #will init a shape from 2 to 6
        match num:
            case 2:
                self.showcase_shape = shapes.Circle(self.window_width / 2, self.window_height / 2, 50, color=(255, 255, 255, 255))
            case 3:
                self.showcase_shape = shapes.Triangle(self.window_width / 2, self.window_height / 2, self.window_width / 2 + 50, self.window_height / 2 + 50, self.window_width / 2 - 50, self.window_height / 2 + 50, color=(255, 255, 255, 255))
            case 4:
                self.showcase_shape = shapes.Rectangle(self.window_width / 2 - 50, self.window_height / 2 - 50, 100, 100, color=(255, 255, 255, 255))
            case 5:
                self.showcase_shape = shapes.Pentagon(self.window_width / 2, self.window_height / 2, 50, color=(255, 255, 255, 255))
            case 6:
                self.showcase_shape = shapes.Hexagon(self.window_width / 2, self.window_height / 2, 50, color=(255, 255, 255, 255))
            case _:
                raise Exception("Invalid showcase number")


    def menu_draw(self):
        if self.pannel_visible:
            for shape in self.visible_pannel_shapes.values():
                shape.draw()
        else:
            for shape in self.hidden_pannel_shapes.values():
                shape.draw()
    

if __name__ == "__main__":
    a = Menu()