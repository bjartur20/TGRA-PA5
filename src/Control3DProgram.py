from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.view_matrix.look(Point(0.0, 2.0, 3.0), Point(0.0, 0.0, 0.0), Vector(0.0, 1.0, 0.0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.fov = pi / 2
        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 10)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.sphere = Sphere(24, 48)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.LEFT_key_down = False
        self.RIGHT_key_down = False

        self.light_position = Point(0.0, 0.0, 5.0)
        self.light_position_factor = 0.0

        self.my_cube_position = Point(0.0, 0.0, 0.0)
        self.my_cube_position_factor = 0.0



## UPDATE ##

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        if(self.LEFT_key_down):
            self.view_matrix.yaw(pi * delta_time)
        if(self.RIGHT_key_down):
            self.view_matrix.yaw(-pi * delta_time)

        self.light_position_factor += delta_time * pi / 10
        self.light_position.x = -cos(self.light_position_factor) * 5.0
        self.light_position.y = 3.0 + sin(self.light_position_factor) * 5.0

        self.my_cube_position_factor += delta_time * pi
        self.my_cube_position.x = cos(self.my_cube_position_factor)



## DISPLAY ##

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        # self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        # self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        self.shader.set_light_position(self.light_position)

        self.model_matrix.load_identity()

    ## FIRST CUBE ##

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.my_cube_position.x, self.my_cube_position.y, self.my_cube_position.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()


    ## FLOOR - TWO PARTS ##

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-1.0, -1.0, 0)
        self.model_matrix.add_scale(1.8, 0.8, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(1.0, -1.0, 0)
        self.model_matrix.add_scale(1.8, 0.8, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        pygame.display.flip()



## PROGRAM EXECUTION ##

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()