import random
from math import pi, sin, cos

from OpenGL.GL import *

from Base3DObjects import Point, Sphere, Color, Material
from Shaders import Shader3D
from Matrices import ModelMatrix


class Planet(Sphere):
    def __init__(self, stack: int = 12, slices: int = 24):
        super().__init__(stack, slices)
        self.size = 1
        self.year_len = 1
        self.distance_from_sun = 1
        self.name = ""
        self.day = 0
        self.position = 0
        self.material = Material()
        self.base_texture_id = 1
        self.specular_id = None
        self.dark_id = None
        self.atmosphere_id = None
        self.random_start = random.randint(0, 10000)  # Makes all planets start at a different place

    def update(self, t: int):
        self.position = (t + self.random_start) / self.year_len
        self.day = self.position * self.year_len / 10

    def set_distance_from_sun(self, dist: float):
        self.distance_from_sun = dist * 10

    def set_year(self, year: int):
        self.year_len = year

    def set_size(self, size: int):
        self.size = size

    def set_name(self, name: str):
        self.name = name

    def set_material(self, r, g, b):
        self.material = Material(Color(r, g, b))

    def set_texture(self, texture_id: int):
        self.base_texture_id = texture_id

    def set_spec_texture(self, texture_id: int):
        self.specular_id = texture_id

    def set_dark_texture(self, texture_id: int):
        self.dark_id = texture_id

    def set_atmosphere_texture(self, texture_id: int):
        self.atmosphere_id = texture_id

    def get_global_coords(self):
        return Point(
            self.distance_from_sun * cos(self.position * 2 * pi),
            0.0,
            -self.distance_from_sun * sin(self.position * 2 * pi),
        )

    def draw(self):
        super().draw()

    def display(self, model_matrix: ModelMatrix, shader: Shader3D):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.base_texture_id)
        shader.set_base_texture(0)
        if self.specular_id:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.specular_id)
            shader.set_specular_texture(1)
            self.material.specular = Color(1.0, 1.0, 1.0)
            self.material.shininess = 100
        if self.dark_id:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, self.dark_id)
            shader.set_dark_side_texture(2)
        if self.atmosphere_id:
            glActiveTexture(GL_TEXTURE3)
            glBindTexture(GL_TEXTURE_2D, self.atmosphere_id)
            shader.set_atmosphere_texture(3)
        model_matrix.push_matrix()
        model_matrix.add_rotation_y(self.position * 2 * pi)
        shader.set_material(self.material)
        model_matrix.add_translation(self.distance_from_sun, 0, 0)
        model_matrix.add_rotation_z(pi)
        model_matrix.add_rotation_y(self.day * 2 * pi)
        model_matrix.add_scale(self.size, self.size, self.size)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw()
        model_matrix.pop_matrix()
        if self.atmosphere_id:
            glActiveTexture(GL_TEXTURE3)
            glBindTexture(GL_TEXTURE_2D, 0)
            shader.set_atmosphere_texture(3)
        if self.dark_id:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, 0)  # Reset dark side texture
            shader.set_dark_side_texture(2)
        if self.specular_id:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, 0)  # Reset specular
            shader.set_specular_texture(1)
