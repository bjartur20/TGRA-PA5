
from OpenGL.GL import *

import numpy

from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, other):
        return Point(self.x * other, self.y * other, self.y * other)

    def values(self):
        return self.x, self.y, self.z, 1.0


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)


class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def values(self):
        return self.r, self.g, self.b, self.a


class Material:
    def __init__(self, diffuse=None, specular=None, shininess=None, ambient=None, emission=None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse is None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular is None else specular
        self.shininess = 1 if shininess is None else shininess
        self.ambient = Color(0.0, 0.0, 0.0) if ambient is None else ambient
        self.emission = Color(0.0, 0.0, 0.0) if emission is None else emission


class Light:
    def __init__(self, position=None, ambient=None, diffuse=None, specular=None, attenuation=None):
        self.position = Point(0.0, 0.0, 0.0) if position is None else position
        self.ambient = Color(0.0, 0.0, 0.0) if ambient is None else ambient
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse is None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular is None else specular
        self.attenuation = Vector(1.0, 0.0, 0.0) if attenuation is None else attenuation


class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0]

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    @staticmethod
    def draw():
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)


class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        # self.index_arrays = dict()
        self.mesh_materials = dict()
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()

    def add_vertex(self, mesh_id, position, normal, uv=None):
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z]
        self.vertex_counts[mesh_id] += 1

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        self.materials[mat_id] = mat

    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
            self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id], dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]
            shader.set_material(material)
            # shader.set_material_diffuse(material.diffuse)
            # shader.set_material_specular(material.specular)
            # shader.set_material_shininess(material.shininess)
            shader.set_attribute_buffers(self.vertex_buffer_ids[mesh_id])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)


class Sphere:
    def __init__(self, stacks: int = 12, slices: int = 24):
        self.vertex_array: list = []
        self.slices: int = slices

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count: int = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                self.vertex_array.append(sin(stack_angle) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle))
                self.vertex_array.append(sin(stack_angle) * sin(slice_angle))

                self.vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle + stack_interval))
                self.vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                self.vertex_count += 2

    def set_vertices(self, shader):
        shader.set_position_attribute(self.vertex_array)
        shader.set_normal_attribute(self.vertex_array)

    def draw(self):
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
