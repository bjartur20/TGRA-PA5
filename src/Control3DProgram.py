from OpenGL.GL import *

from math import *
from random import uniform

import pygame
from pygame.locals import *

import sys
import time

from Shaders import Shader3D
from Matrices import ModelMatrix, ViewMatrix, ProjectionMatrix
from Base3DObjects import Point, Vector, Cube, Sphere, Color, Light, Material
from Planet import Planet
from Space import Space
from ObjLoader import ObjLoader

EARTH_SIZE = 0.5
EARTH_SPEED = 0.1
WINDOW_SIZE = (1920, 1080)  # (800, 600)


class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode(WINDOW_SIZE, pygame.OPENGL | pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.view_matrix.look(
            Point(0.0, 2.0, 3.0), Point(0.0, 0.0, 0.0), Vector(0.0, 1.0, 0.0)
        )
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.fov = pi / 2
        self.projection_matrix.set_perspective(
            self.fov, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.5, 10
        )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.sphere = Sphere(24, 48)
        self.planets = [Planet(24, 48) for i in range(8)]
        self.sun = Planet(24, 48)
        self.space = Space()
        self.ship = ObjLoader.load_obj_file(
            sys.path[0] + "/Models/SpaceShip", "tie_fighter.obj"
        )

        # Bezier curve for the ship
        self.ship_pos = Point(10.0, 0.0, 00.0)
        self.ship_start_moving = 5
        self.ship_end_moving = 120
        # Insert starting point and end point
        self.bezier_points = [Point(10.0, 0.0, 0.0), Point(10.0, 0.0, 0.0)]
        # Insert a bunch of random points between the two
        for _ in range(100):
            self.bezier_points.insert(
                3, Point(uniform(-200, 200), uniform(-200, 200), uniform(-200, 200))
            )

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.views = [False] * 9

        self.look_x = 0
        self.look_y = 0

        self.speed = 5

        self.light_position = Point(0.0, 0.0, 0.0)
        self.light_position_factor = 0.0

        self.my_cube_position = Point(0.0, 0.0, 0.0)
        self.my_cube_position_factor = 0.0

        scalar = 1 / 75
        # Configure each planet
        # Mercury
        self.planets[0].set_name("Mercury")
        self.planets[0].set_size(EARTH_SIZE / 3)
        self.planets[0].set_year(88 * scalar)
        self.planets[0].set_distance_from_sun(0.4)
        self.planets[0].set_material(0.86, 0.81, 0.79)
        self.planets[0].set_texture(self.load_texture("2k_mercury.jpg"))
        # Venus
        self.planets[1].set_name("Venus")
        self.planets[1].set_size(EARTH_SIZE - 0.1)
        self.planets[1].set_year(225 * scalar)
        self.planets[1].set_distance_from_sun(0.7)
        self.planets[1].set_material(0.65, 0.49, 0.11)
        self.planets[1].set_texture(self.load_texture("2k_venus_surface.jpg"))
        # # Earth
        self.planets[2].set_name("Earth")
        self.planets[2].set_size(EARTH_SIZE)
        self.planets[2].set_year(365 * scalar)
        self.planets[2].set_distance_from_sun(1)
        self.planets[2].set_material(0.49, 0.64, 0.49)
        self.planets[2].set_texture(self.load_texture("2k_earth_daymap.jpg"))
        # # Mars
        self.planets[3].set_name("Mars")
        self.planets[3].set_size(EARTH_SIZE / 2)
        self.planets[3].set_year(687 * scalar)
        self.planets[3].set_distance_from_sun(1.5)
        self.planets[3].set_material(0.76, 0.27, 0.05)
        self.planets[3].set_texture(self.load_texture("2k_mars.jpg"))
        # # Jupiter
        self.planets[4].set_name("Jupiter")
        self.planets[4].set_size(EARTH_SIZE * 11)
        self.planets[4].set_year(4329 * scalar)
        self.planets[4].set_distance_from_sun(5.2)
        self.planets[4].set_material(0.89, 0.86, 0.80)
        self.planets[4].set_texture(self.load_texture("2k_jupiter.jpg"))
        # # Saturn
        self.planets[5].set_name("Saturn")
        self.planets[5].set_size(EARTH_SIZE * 9)
        self.planets[5].set_year(10738 * scalar)
        self.planets[5].set_distance_from_sun(9.5)
        self.planets[5].set_material(0.89, 0.88, 0.75)
        self.planets[5].set_texture(self.load_texture("2k_saturn.jpg"))
        # # Uranus
        self.planets[6].set_name("Uranus")
        self.planets[6].set_size(EARTH_SIZE * 4)
        self.planets[6].set_year(30569 * scalar)
        self.planets[6].set_distance_from_sun(19.8)
        self.planets[6].set_material(0.73, 0.88, 0.89)
        self.planets[6].set_texture(self.load_texture("2k_uranus.jpg"))
        # # Naptune
        self.planets[7].set_name("Neptune")
        self.planets[7].set_size(EARTH_SIZE * 4 - 0.01)
        self.planets[7].set_year(59769 * scalar)
        self.planets[7].set_distance_from_sun(30.1)
        self.planets[7].set_material(0.29, 0.44, 0.87)
        self.planets[7].set_texture(self.load_texture("2k_neptune.jpg"))

        self.light = Light(
            self.light_position,
            Color(0.8, 0.8, 0.8),
            Color(0.8, 0.8, 0.8),
            Color(0.8, 0.8, 0.8),
        )
        self.sun_material = Material(emission=Color(0.8, 0.7, 0.0))
        self.skybox_material = Material(emission=Color(0.2, 0.2, 0.2))

        self.skybox_tex = self.load_texture("stars.jpg")
        self.white_tex = self.load_texture("white.png")
        self.black_tex = self.load_texture("black.png")
        self.sun_tex = self.load_texture("2k_sun.jpg")

    @staticmethod
    def load_texture(filename: str):
        surface = pygame.image.load(sys.path[0] + f"/textures/{filename}")
        tex_string = pygame.image.tostring(surface, "RGBA", True)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            tex_string,
        )
        return tex_id

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

    def bezier_curve(self, points: list, curr_time: float):
        t = (curr_time - self.ship_start_moving) / (
            self.ship_end_moving - self.ship_start_moving
        )

        new_points = points
        while len(new_points) > 1:
            new_new_points = []
            for i1 in range(0, len(new_points) - 1):
                new_new_points += [(1 - t) * new_points[i1] + t * new_points[i1 + 1]]
            new_points = new_new_points

        return new_points[0]

    ## UPDATE ##

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        curr_time = pygame.time.get_ticks() / 1000

        # Individual planet/space ship view
        if any(self.views):
            # Space ship view
            if self.views[8]:
                self.view_matrix.look(
                    Point(self.ship_pos.x + 1, self.ship_pos.y, self.ship_pos.z),
                    self.ship_pos,
                    Vector(0, 1, 0),
                )
            # Planetary view
            else:
                planet = [i for i, x in enumerate(self.views) if x][0]
                planet_pos = self.planets[planet].get_global_coords()
                self.view_matrix.look(
                    Point(
                        planet_pos.x + (self.planets[planet].size + 2) * 2,
                        planet_pos.y,
                        planet_pos.z,
                    ),
                    planet_pos,
                    Vector(0.0, 1.0, 0.0),
                )
        # Free Movement
        else:
            self.spectator_movement(delta_time)

        # TODO: USE DELTA TIME FOR UPDATING PLANET POSITIONS
        for planet in self.planets:
            planet.update(curr_time)

        self.light_position_factor += delta_time * pi / 10
        self.light_position.x = -cos(self.light_position_factor) * 5.0
        self.light_position.y = 3.0 + sin(self.light_position_factor) * 5.0

        self.my_cube_position_factor += delta_time * pi
        self.my_cube_position.x = cos(self.my_cube_position_factor)

        # Bezier curve ship movement
        self.ship_pos = self.bezier_curve(self.bezier_points, curr_time)

    ## DISPLAY ##

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.projection_matrix.set_perspective(
            pi / 2,  # FOV
            WINDOW_SIZE[0] / WINDOW_SIZE[1],  # Aspect ratio
            0.1,  # Near plane
            1000,  # Far plane
        )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)

        # Setup light
        self.shader.set_light(self.light)
        self.shader.set_global_ambient(0.0, 0.0, 0.0)

        self.model_matrix.load_identity()

        # Space ship
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.white_tex)
        self.shader.set_base_texture(0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(
            self.ship_pos.x, self.ship_pos.y, self.ship_pos.z
        )
        self.model_matrix.add_scale(0.01, 0.01, 0.01)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.ship.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Sun
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.sun_tex)
        self.shader.set_base_texture(0)

        self.shader.set_material(self.sun_material)
        self.sphere.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(2, 2, 2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sun.draw()
        self.model_matrix.pop_matrix()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.white_tex)
        self.shader.set_base_texture(0)
        # Planets
        self.model_matrix.push_matrix()
        for planet in self.planets:
            planet.display(self.model_matrix, self.shader)
        self.model_matrix.pop_matrix()

        # Skybox/stars TODO: Add texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.skybox_tex)
        self.shader.set_base_texture(0)

        self.shader.set_material(self.skybox_material)
        self.space.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(1000, 1000, 1000)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.space.draw()
        self.model_matrix.pop_matrix()

        pygame.display.flip()

    def change_view(self, key_idx):
        for i in range(len(self.views)):
            if i == key_idx:
                self.views[i] = not self.views[i]
            else:
                self.views[i] = False

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

                    if event.key == K_1:
                        self.change_view(0)
                    if event.key == K_2:
                        self.change_view(1)
                    if event.key == K_3:
                        self.change_view(2)
                    if event.key == K_4:
                        self.change_view(3)
                    if event.key == K_5:
                        self.change_view(4)
                    if event.key == K_6:
                        self.change_view(5)
                    if event.key == K_7:
                        self.change_view(6)
                    if event.key == K_8:
                        self.change_view(7)
                    if event.key == K_9:
                        self.change_view(8)

                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False

            self.look_x, self.look_y = pygame.mouse.get_rel()
            self.look_y *= -0.3
            self.look_x *= -0.3

            if len(events) == 0:
                self.look_x = self.look_y = 0

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
