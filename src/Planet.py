from Base3DObjects import Sphere

class Planet(Sphere):
    def __init__(self, stack=12, slices=24):
        super().__init__(stack, slices)
        self.size = 1
        self.speed = 1
        self.name = ""

    def set_speed(self, speed):
        self.speed = speed

    def set_size(self, size):
        self.size = size

    def set_name(self, name):
        self.name = name

    def draw(self, shader):
        super().draw(shader)

    def display(self, model_matrix, shader, i):
        model_matrix.push_matrix()
        model_matrix.add_translation(10*i, 0, 0)
        model_matrix.add_scale(self.size, self.size, self.size)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader) 
        model_matrix.pop_matrix()