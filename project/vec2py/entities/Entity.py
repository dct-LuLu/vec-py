class Entity:
    instances: set = set()

    def __init__(self, x_velocity=0, y_velocity=0, angular_velocity=0):
        self._mass = 1 # La masse de l'entité
        force = -9.8# La force de l'entité
        self._x_velocity = x_velocity
        self._x_acceleration = 0 # L'accélération de l'entité

        self._y_velocity = y_velocity
        self._y_acceleration = (force / self._mass) # L'accélération de l'entité
        
        self._angular_velocity = angular_velocity # Jamais négatif et jamais supérieur à 360
        self._angular_acceleration = 0 # L'accélération angulaire de l'entité


        self.fixed = False # Si l'entité est fixe (ne bouge pas)
        self.maneuverable = True # Si l'entité peut être contrôlée par le joueur
        Entity.instances.add(self)

    def full_stop(self):
        self._x_velocity = 0
        self._y_velocity = 0
        self._angular_velocity = 0

    @classmethod
    def getEntities(cls):
        return cls.instances

    @classmethod
    def get_movables(cls):
        return [entity for entity in cls.instances if not entity.fixed]

    @property
    def x_velocity(self):
        """The x velocity of the entity."""
        return self._x_velocity
    
    @x_velocity.setter
    def x_velocity(self, value):
        self._x_velocity = value
        

    