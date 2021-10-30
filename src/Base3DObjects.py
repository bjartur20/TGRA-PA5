
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
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Material:
    def __init__(self, diffuse = None, specular = None, shininess = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.shininess = 1 if shininess == None else shininess

class Cube:
    def __init__(self):
        vertex_array = [-0.5, -0.5, -0.5, 0.0, 0.0, -1.0,
                               -0.5, 0.5, -0.5,  0.0, 0.0, -1.0,
                               0.5, 0.5, -0.5,   0.0, 0.0, -1.0,
                               0.5, -0.5, -0.5,  0.0, 0.0, -1.0,
                               -0.5, -0.5, 0.5,  0.0, 0.0, 1.0, 
                               -0.5, 0.5, 0.5,   0.0, 0.0, 1.0, 
                               0.5, 0.5, 0.5,    0.0, 0.0, 1.0, 
                               0.5, -0.5, 0.5,   0.0, 0.0, 1.0, 
                               -0.5, -0.5, -0.5, 0.0, -1.0, 0.0,
                               0.5, -0.5, -0.5,  0.0, -1.0, 0.0,
                               0.5, -0.5, 0.5,   0.0, -1.0, 0.0,
                               -0.5, -0.5, 0.5,  0.0, -1.0, 0.0,
                               -0.5, 0.5, -0.5,  0.0, 1.0, 0.0, 
                               0.5, 0.5, -0.5,   0.0, 1.0, 0.0, 
                               0.5, 0.5, 0.5,    0.0, 1.0, 0.0, 
                               -0.5, 0.5, 0.5,   0.0, 1.0, 0.0, 
                               -0.5, -0.5, -0.5, -1.0, 0.0, 0.0,
                               -0.5, -0.5, 0.5,  -1.0, 0.0, 0.0,
                               -0.5, 0.5, 0.5,   -1.0, 0.0, 0.0,
                               -0.5, 0.5, -0.5,  -1.0, 0.0, 0.0,
                               0.5, -0.5, -0.5,  1.0, 0.0, 0.0, 
                               0.5, -0.5, 0.5,   1.0, 0.0, 0.0, 
                               0.5, 0.5, 0.5,    1.0, 0.0, 0.0, 
                               0.5, 0.5, -0.5,    1.0, 0.0, 0.0  ]
                            
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)
        # glBindVertexArray(0)
        # glBindBuffer(GL_ARRAY_BUFFER, 0)



class Sphere:
    def __init__(self, stacks = 12, slices = 24):
        self.slices = slices
        self.vertex_count = 0

        vertex_array = []

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                for _ in range(2):
                    vertex_array.append(sin(stack_angle) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle))
                    vertex_array.append(sin(stack_angle) * sin(slice_angle))

                for _ in range(2):
                    vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle + stack_interval))
                    vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                self.vertex_count += 2

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)



    def draw(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        # glBindVertexArray(0)
        # glBindBuffer(GL_ARRAY_BUFFER, 0)

