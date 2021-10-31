from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

from Planet import Planet

EARTH_SIZE = 0.5
EARTH_SPEED = 1

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
        # self.planet = Planet(24, 48)
        self.planets = [Planet(24, 48) for i in range(8)]
        self.sun = Planet(24, 48)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False

        self.look_x = 0
        self.look_y = 0

        self.planet_rotation = 0
        self.speed = 2

        self.light_position = Point(0.0, 0.0, 5.0)
        self.light_position_factor = 0.0

        self.my_cube_position = Point(0.0, 0.0, 0.0)
        self.my_cube_position_factor = 0.0

        # Configure each planet
        # Mercury
        self.planets[0].set_name("Mercury")
        self.planets[0].set_size(EARTH_SIZE/3)
        # Venus
        self.planets[1].set_name("Venus")
        self.planets[1].set_size(EARTH_SIZE-0.1)
        # Earth
        self.planets[2].set_name("Earth")
        self.planets[2].set_size(EARTH_SIZE)
        # Mars
        self.planets[3].set_name("Mars")
        self.planets[3].set_size(EARTH_SIZE/2)
        # Jupiter
        self.planets[4].set_name("Jupiter")
        self.planets[4].set_size(EARTH_SIZE*11)
        # Saturn
        self.planets[5].set_name("Saturn")
        self.planets[5].set_size(EARTH_SIZE*9)
        # Uranus
        self.planets[6].set_name("Uranus")
        self.planets[6].set_size(EARTH_SIZE*4)
        # Naptune
        self.planets[7].set_name("Neptune")
        self.planets[7].set_size(EARTH_SIZE*4-0.01)

    def spectator_movement(self, delta_time):
        # Movement
        if self.W_key_down:
            self.view_matrix.slide(0, 0, -self.speed * delta_time)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, self.speed * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(-self.speed * delta_time, 0, 0)
        if self.D_key_down:
            self.view_matrix.slide(self.speed * delta_time, 0, 0)

        if self.look_x:
            self.view_matrix.yaw(self.look_x * delta_time)
        if self.look_y:
            self.view_matrix.pitch(self.look_y * delta_time)

## UPDATE ##

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        # if(self.LEFT_key_down):
        #     self.view_matrix.yaw(pi * delta_time)
        # if(self.RIGHT_key_down):
        #     self.view_matrix.yaw(-pi * delta_time)

        self.spectator_movement(delta_time)

        self.planet_rotation += pi * delta_time 
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
        self.projection_matrix.set_perspective(
                    pi/2,    # FOV
                    800/600, # Aspect ratio
                    0.1,     # Near plane
                    50)      # Far plane
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        self.shader.set_light_position(self.light_position)

        self.model_matrix.load_identity()

        # Sun
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(2, 2, 2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sun.draw(self.shader)
        self.model_matrix.pop_matrix()




        # Planets
        self.model_matrix.push_matrix()
        # self.model_matrix.add_rotation_y(self.planet_rotation/pi)
        for idx, planet in enumerate(self.planets):
            print(planet.name)
            planet.display(self.model_matrix, self.shader, idx+1)
            # self.model_matrix.push_matrix()
            # self.model_matrix.add_translation(5*i, 0, 0)
            # self.model_matrix.add_rotation_y(self.my_cube_position_factor)
            # self.model_matrix.add_rotation_y(self.my_cube_position_factor)
            # self.shader.set_model_matrix(self.model_matrix.matrix)
            # self.planet.draw(self.shader) 
            # self.model_matrix.pop_matrix()
        self.model_matrix.pop_matrix()

        pygame.display.flip()

## PROGRAM EXECUTION ##

    def program_loop(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        exiting = False
        while not exiting:
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                    
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False

                elif event.type == pygame.MOUSEMOTION:
                    self.look_x, self.look_y = pygame.mouse.get_rel()
                    self.look_y *= -1
                    self.look_x *= -1
            
            if len(events) == 0:
                self.look_x = self.look_y = 0

            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()