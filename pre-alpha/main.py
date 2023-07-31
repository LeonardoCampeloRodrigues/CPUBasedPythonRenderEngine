import pygame
from math import radians
from utils import *
from time import time

color = [255, 0, 0]

faces = [[[0, 1, 2], color_random()], [[1, 3, 2], color_random()], #Up
         [[5, 1, 0], color_random()], [[0, 4, 5], color_random()], #Right       
         [[5, 6, 3], color_random()], [[3, 1, 5], color_random()], #Back      
         [[6, 7, 2], color_random()], [[2, 3, 6], color_random()], #Left                                                         
         [[4, 2, 7], color_random()], [[4, 0, 2], color_random()], #Front
         [[6, 4, 7], color_random()], [[6, 5, 4], color_random()]] #Bellow
 
verticies = [[ 1,  1,  1], 
             [ 1,  1, -1],
             [-1,  1,  1],
             [-1,  1, -1],
             [ 1, -1,  1],
             [ 1, -1, -1],
             [-1, -1, -1],
             [-1, -1,  1]]

verticies, faces = load_obj("models/forest.obj", face_color = [255, 255, 255])

znear = -1
zfar = -1000
obj_world_location = [0, 0, -12]

is_moving_forward = False
is_moving_backward = False
is_moving_right = False
is_moving_left = False
is_moving_up = False
is_moving_down = False
is_turning_right = False
is_turning_left = False
is_turning_down = False
is_turning_up = False
camera_forward, camera_right = [0, 0, -1],  [1, 0, 0]
camera_down = cross_product(camera_forward, camera_right)
camera_location = [0, 0, 0]
camera_rotation_x, camera_rotation_y = 0, 0
movement_factor = 0.1
rotation_factor = 1


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
H_FOV = 90
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True	
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                is_moving_left = True
            elif event.key == pygame.K_d:
                is_moving_right = True
            elif event.key == pygame.K_w:
                is_moving_forward = True
            elif event.key == pygame.K_s:
                is_moving_backward = True
            elif event.key == pygame.K_SPACE:
                is_moving_up = True
            elif event.key == pygame.K_LCTRL:
                is_moving_down = True
            elif event.key == pygame.K_e:
                is_turning_right = True
            elif event.key == pygame.K_q:
                is_turning_left = True
            elif event.key == pygame.K_r:
                is_turning_down = True
            elif event.key == pygame.K_f:
                is_turning_up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                is_moving_left = False
            elif event.key == pygame.K_d:
                is_moving_right = False
            elif event.key == pygame.K_w:
                is_moving_forward = False
            elif event.key == pygame.K_s:
                is_moving_backward = False  
            elif event.key == pygame.K_SPACE:
                is_moving_up = False
            elif event.key == pygame.K_LCTRL:
                is_moving_down = False
            elif event.key == pygame.K_e:
                is_turning_right = False
            elif event.key == pygame.K_q:
                is_turning_left = False
            elif event.key == pygame.K_r:
                is_turning_down = False
            elif event.key == pygame.K_f:
                is_turning_up = False

    light = [-1, 0, 0]
    light = normalize(light)

    if is_turning_left:
        rotate_y([camera_forward], -rotation_factor)
        rotate_y([camera_right], -rotation_factor)
        camera_forward = normalize(camera_forward)
        camera_right = normalize(camera_right)
        camera_down = normalize(cross_product(camera_forward, camera_right))
        camera_rotation_y += -rotation_factor
    if is_turning_right:
        rotate_y([camera_forward], rotation_factor)
        rotate_y([camera_right], rotation_factor)
        camera_forward = normalize(camera_forward)
        camera_right = normalize(camera_right)
        camera_down = normalize(cross_product(camera_forward, camera_right))
        camera_rotation_y += rotation_factor 

    if is_moving_left:
         move_along_vector(camera_location, negative_vector(camera_right), movement_factor)
    if is_moving_right:
         move_along_vector(camera_location, camera_right, movement_factor)
    if is_moving_forward:
         move_along_vector(camera_location, camera_forward, movement_factor)
    if is_moving_backward:
         move_along_vector(camera_location, negative_vector(camera_forward), movement_factor)
    if is_moving_up:
        move_along_vector(camera_location, negative_vector(camera_down), movement_factor)
    if is_moving_down:
        move_along_vector(camera_location, camera_down, movement_factor)

    screen.fill((0, 0, 0))  
  
    f = faces
    v = []
    for vertex in verticies:
        v.append(vertex.copy())    


    #Local Transformations
    #rotate_y(v, 10*time())

    #Global Transformations
    translate(v, obj_world_location[0], obj_world_location[1], obj_world_location[2])
        
    #View Transformations
    translate(v, -camera_location[0], -camera_location[1], -camera_location[2])
    rotate_y([light], -camera_rotation_y)
    rotate_y(v, -camera_rotation_y)
 
    #Render Pipeline
    f = cull(v, f)
    f = shade_flat(v, f, light)   
    calculate_average_xyz(v, f)
    f = clip(f, znear, zfar, screen, H_FOV)
    sort_faces_by_depth(f)
    perspective_projection(f, v, screen, H_FOV)
    draw_faces(v, f, screen, render_faces=True, render_wire_frame=False, render_verticies=False)

    pygame.display.flip()
    clock.tick()
    pygame.display.set_caption("FPS:" + str(int(clock.get_fps())))
