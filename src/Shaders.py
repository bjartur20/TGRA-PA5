from OpenGL.GL import *
import OpenGL.GLU
from math import *  # trigonometry

import sys

from Base3DObjects import *


class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/shaders/simple3D.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print(
                "Couldn't compile vertex shader\nShader compilation Log:\n"
                + str(glGetShaderInfoLog(vert_shader))
            )

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/shaders/simple3D.frag")
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print(
                "Couldn't compile fragment shader\nShader compilation Log:\n"
                + str(glGetShaderInfoLog(frag_shader))
            )

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)
        result = glGetProgramiv(self.renderingProgramID, GL_LINK_STATUS)
        if result != 1:  # program didn't link
            print(
                "Couldn't link shader program\nShader link Log:\n"
                + str(glGetProgramInfoLog(self.renderingProgramID))
            )

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.modelMatrixLoc = glGetUniformLocation(
            self.renderingProgramID, "u_model_matrix"
        )
        self.viewMatrixLoc = glGetUniformLocation(
            self.renderingProgramID, "u_view_matrix"
        )
        self.projectionMatrixLoc = glGetUniformLocation(
            self.renderingProgramID, "u_projection_matrix"
        )

        self.lightPosLoc = glGetUniformLocation(
            self.renderingProgramID, "u_light_position"
        )
        self.lightAmbientLoc = glGetUniformLocation(
            self.renderingProgramID, "u_light_ambient"
        )
        self.lightDiffuseLoc = glGetUniformLocation(
            self.renderingProgramID, "u_light_diffuse"
        )
        self.lightSpecularLoc = glGetUniformLocation(
            self.renderingProgramID, "u_light_specular"
        )
        self.lightAttenuationLoc = glGetUniformLocation(
            self.renderingProgramID, "U_light_attenuation"
        )
        self.globalAmbientLoc = glGetUniformLocation(
            self.renderingProgramID, "u_global_ambient"
        )

        self.materialAmbientLoc = glGetUniformLocation(
            self.renderingProgramID, "u_material_ambient"
        )
        self.materialDiffuseLoc = glGetUniformLocation(
            self.renderingProgramID, "u_material_diffuse"
        )
        self.materialSpecularLoc = glGetUniformLocation(
            self.renderingProgramID, "u_material_specular"
        )
        self.materialEmissionLoc = glGetUniformLocation(
            self.renderingProgramID, "u_material_emission"
        )
        self.materialShininessLoc = glGetUniformLocation(
            self.renderingProgramID, "u_material_shininess"
        )

        self.textureBaseLoc = glGetUniformLocation(
            self.renderingProgramID, "u_tex_base"
        )
        self.textureSpecLoc = glGetUniformLocation(
            self.renderingProgramID, "u_tex_specular"
        )
        self.textureDarkLoc = glGetUniformLocation(
            self.renderingProgramID, "u_tex_dark_side"
        )
        self.textureAtmosLoc = glGetUniformLocation(
            self.renderingProgramID, "u_tex_atmosphere"
        )

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_light(self, light: Light):
        glUniform4f(self.lightPosLoc, *light.position.values())
        glUniform4f(self.lightAmbientLoc, *light.ambient.values())
        glUniform4f(self.lightDiffuseLoc, *light.diffuse.values())
        glUniform4f(self.lightSpecularLoc, *light.specular.values())

    def set_global_ambient(self, r, g, b):
        glUniform4f(self.globalAmbientLoc, r, g, b, 1.0)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_base_texture(self, number: int):
        glUniform1i(self.textureBaseLoc, number)

    def set_specular_texture(self, number: int):
        glUniform1i(self.textureSpecLoc, number)

    def set_dark_side_texture(self, number: int):
        glUniform1i(self.textureDarkLoc, number)

    def set_atmosphere_texture(self, number: int):
        glUniform1i(self.textureAtmosLoc, number)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_material(self, material: Material):
        glUniform4f(self.materialAmbientLoc, *material.ambient.values())
        glUniform4f(self.materialDiffuseLoc, *material.diffuse.values())
        glUniform4f(self.materialSpecularLoc, *material.specular.values())
        glUniform4f(self.materialEmissionLoc, *material.emission.values())
        glUniform1f(self.materialShininessLoc, material.shininess)

    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(
            self.positionLoc,
            3,
            GL_FLOAT,
            False,
            6 * sizeof(GLfloat),
            OpenGL.GLU.ctypes.c_void_p(0),
        )
        glVertexAttribPointer(
            self.normalLoc,
            3,
            GL_FLOAT,
            False,
            6 * sizeof(GLfloat),
            OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)),
        )
        glVertexAttribPointer(
            self.uvLoc,
            2,
            GL_FLOAT,
            False,
            6 * sizeof(GLfloat),
            OpenGL.GLU.ctypes.c_void_p(2 * sizeof(GLfloat)),
        )
