class Walls:

    def check(self, obj):
        if obj.x > self.window_width:
            obj.x -= (obj.x-self.window_width+1)
            obj.x_velocity = -obj.x_velocity

        elif obj.x < 0:
            obj.x -= obj.x-1
            obj.x_velocity = -obj.x_velocity

        if obj.y > self.window_height:
            obj.y -= (obj.y-self.window_height+1)
            obj.y_velocity = -obj.y_velocity

        elif obj.y < 0:
            obj.y -= obj.y-1
            obj.y_velocity = -obj.y_velocity
