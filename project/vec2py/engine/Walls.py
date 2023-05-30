class Walls:

    @staticmethod
    def check(sup, obj):
        if obj.x > sup.window_width-0:
            obj.x -= (obj.x-sup.window_width+1)
            obj.x_velocity = -obj.x_velocity

        elif obj.x < 0:
            obj.x -= obj.x-1
            obj.x_velocity = -obj.x_velocity

        if obj.y > sup.window_height-0:
            obj.y -= (obj.y-sup.window_height+1)
            obj.y_velocity = -obj.y_velocity

        elif obj.y < 0:
            obj.y -= obj.y-1
            obj.y_velocity = -obj.y_velocity
