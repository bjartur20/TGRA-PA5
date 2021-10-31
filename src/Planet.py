from math import pi

from Base3DObjects import Sphere
from Shaders import Shader3D
from Matrices import ModelMatrix

class Planet(Sphere):
    def __init__(self, stack: int = 12, slices: int = 24):
        super().__init__(stack, slices)
        self.size = 1
        self.year_len = 1
        self.distance_from_sun = 1
        self.name = ""
        self.position = 0
        self.color = (1.0, 1.0, 1.0)

    def update(self, t: int):
        self.position = (t / self.year_len)

    def set_distance_from_sun(self, dist: float):
        self.distance_from_sun = dist

    def set_year(self, year: int):
        self.year_len = year

    def set_size(self, size: int):
        self.size = size

    def set_name(self, name: str):
        self.name = name
    
    def set_color(self, r, g, b):
        self.color = (r, g, b)

    def get_global_coords(self):
        pass

    def draw(self, shader: Shader3D):
        super().draw(shader)

    def display(self, model_matrix: ModelMatrix, shader: Shader3D):
        model_matrix.push_matrix()
        model_matrix.add_rotation_y(self.position * 2 * pi)
        shader.set_material_diffuse(*self.color)
        model_matrix.add_translation(self.distance_from_sun*10, 0, 0)
        model_matrix.add_scale(self.size, self.size, self.size)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader) 
        model_matrix.pop_matrix()