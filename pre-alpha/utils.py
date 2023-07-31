from math import cos, sin, radians, tan, sqrt, atan
from random import randint
import pygame

def color_random(minimun=0, maximum=255):
    return [randint(minimun, maximum), randint(minimun, maximum), randint(minimun, maximum)]

def rotate_z(verticies, angle):
    for vertex in verticies:
        c = cos(radians(angle))
        s = sin(radians(angle))
        vertex[0], vertex[1] = vertex[0]*c - vertex[1]*s, vertex[0]*s + vertex[1]*c

def rotate_y(verticies, angle):
    for vertex in verticies:
        c = cos(radians(angle))
        s = sin(radians(angle))
        vertex[0], vertex[2] = vertex[0]*c - vertex[2]*s, vertex[0]*s + vertex[2]*c

def rotate_x(verticies, angle):
    for vertex in verticies:
        c = cos(radians(angle))
        s = sin(radians(angle))
        vertex[1], vertex[2] = vertex[1]*c + vertex[2]*s, -vertex[1]*s + vertex[2]*c

def scale(verticies, sx=1, sy=1, sz=1):
    for vertex in verticies:
        vertex[0] *= sx
        vertex[1] *= sy
        vertex[2] *= sz

def translate(verticies, x = 0, y = 0, z = 0):
    for vertex in verticies:
        vertex[0] += x
        vertex[1] += y
        vertex[2] += z

def cross_product(a, b):
    return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def perspective_projection(faces, verticies, screen: pygame.Surface, horizontal_fov, d = 1):
    #Avoid double projection creating a set of the verticies index instead of looping the faces
    index_verticies = set()
    for face in faces:
        index_verticies.update(face[0])

    V_w = 2*d*tan(radians(horizontal_fov)/2)
    V_h = screen.get_height()/screen.get_width()*V_w
    for index in index_verticies:
        vertex = verticies[index]
        vertex[0], vertex[1] = vertex[0]*d/abs(vertex[2]), vertex[1]*d/abs(vertex[2]) 
        vertex[0], vertex[1] = screen.get_width()/V_w*vertex[0] + screen.get_width()/2, -screen.get_height()/V_h*vertex[1] + screen.get_height()/2 
        
def cull(verticies, faces):
    done = []
    for face in faces:
        a = verticies[face[0][0]]
        b = verticies[face[0][1]]
        c = verticies[face[0][2]]
        ab = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
        ac = [a[0] - c[0], a[1] - c[1], a[2] - c[2]]
        if dot(cross_product(ab,ac), a) > 0:
            continue
        done.append(face)
    return done

def draw_faces(verticies, faces, screen: pygame.Surface, verticies_color = (255, 0, 255), wire_frame_color = (255, 255, 255), 
               render_faces = True, render_wire_frame = False, render_verticies = False, point_size = 1):
    for face in faces:
        a = verticies[face[0][0]]
        b = verticies[face[0][1]]
        c = verticies[face[0][2]]
        if render_faces:
            pygame.draw.polygon(screen, face[1], [(a[0],a[1]), (b[0],b[1]), (c[0],c[1]), (a[0],a[1])])
        if render_wire_frame:
            pygame.draw.line(screen, wire_frame_color, (a[0],a[1]), (b[0],b[1]), 1)
            pygame.draw.line(screen, wire_frame_color, (b[0],b[1]), (c[0],c[1]), 1)
            pygame.draw.line(screen, wire_frame_color, (c[0],c[1]), (a[0],a[1]), 1)        
        if render_verticies:
            pygame.draw.circle(screen, verticies_color, (a[0], a[1]), point_size)
            pygame.draw.circle(screen, verticies_color, (b[0], b[1]), point_size)
            pygame.draw.circle(screen, verticies_color, (c[0], c[1]), point_size)

def length(vertex):
    return sqrt(vertex[0]**2 + vertex[1]**2 + vertex[2]**2)

def normalize(vertex):
    l = length(vertex)
    return [vertex[0]/l, vertex[1]/l, vertex[2]/l]

def clamp(number, maximum = 1, minimum = 0):
    if number > maximum:
        return maximum
    if number < minimum:
        return minimum
    return number

def shade_flat(verticies, faces, light):
    done = []
    for face in faces:
        a = verticies[face[0][0]]
        b = verticies[face[0][1]]
        c = verticies[face[0][2]]
        ab = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
        ac = [a[0] - c[0], a[1] - c[1], a[2] - c[2]]
        face_direction = normalize(cross_product(ab,ac))
        factor = -dot(face_direction, light)
        r = clamp(face[1][0]*(factor + 1)/2, 255)
        g = clamp(face[1][1]*(factor + 1)/2, 255)
        b = clamp(face[1][2]*(factor + 1)/2, 255)
        done.append([face[0], [r, g, b]])
    return done

def calculate_average_xyz(verticies, faces):
    for face in faces:
        average_x = (verticies[face[0][0]][0] + verticies[face[0][1]][0] + verticies[face[0][2]][0])/3
        average_y = (verticies[face[0][0]][1] + verticies[face[0][1]][1] + verticies[face[0][2]][1])/3
        average_z = (verticies[face[0][0]][2] + verticies[face[0][1]][2] + verticies[face[0][2]][2])/3
        face.append([average_x, average_y, average_z])

def old_sort_faces_by_depth(faces):
    done = False
    while(not done):
        for i in range(len(faces) - 1):
            if faces[i][2][2] > faces[i + 1][2][2]:
                faces[i], faces[i + 1] = faces[i + 1], faces[i]
        for i in range(len(faces) - 1):
            if faces[i][2][2] > faces[i + 1][2][2]:
                done = False
                break
            done = True

def merge(faces, begin, mid, end):
    left = faces[begin:mid]
    right = faces[mid:end]
    top_left, top_right = 0, 0
    for k in range(begin, end):
        if top_left >= len(left):
            faces[k] = right[top_right]
            top_right += 1
        elif top_right >= len(right):
            faces[k] = left[top_left]
            top_left += 1
        elif left[top_left][2][2] < right[top_right][2][2]:
            faces[k] = left[top_left]
            top_left += 1
        else:
            faces[k] = right[top_right]
            top_right += 1

def sort_faces_by_depth(faces, begin=0, end=None):
    if end is None:
        end = len(faces)
    if (end - begin > 1):
        mid = (end + begin)//2
        sort_faces_by_depth(faces, begin, mid)
        sort_faces_by_depth(faces, mid, end)
        merge(faces, begin, mid, end)

def load_obj(filename, face_color = None):
    with open(filename, "r") as f:
        verticies = []
        faces = []
        for line in f:
            if line[0:2] == "v ":
                coordinates = []
                for number in line[2:].split():
                    coordinates.append(float(number))
                verticies.append(coordinates)
            if line[0:2] == "f ":
                face_indicies = []
                for part in line[2:].split():
                    face_indicies.append(int(part.split("/")[0])-1)
                faces.append([face_indicies])
    if not face_color:
        for face in faces:
            face.append(color_random())
    else:
        for face in faces:
            face.append(face_color)
    return verticies, faces

def move_along_vector(position, vector, sensibility):
    position[0] += vector[0]*sensibility
    position[1] += vector[1]*sensibility
    position[2] += vector[2]*sensibility

def negative_vector(vector):
    return [-vector[0], -vector[1], -vector[2]]

def clip(faces, znear, zfar, screen, horizontal_fov, d = 1, error = 2):
    done = []
    V_w = 2*d*tan(radians(horizontal_fov)/2)
    V_h = screen.get_height()/screen.get_width()*V_w
    vertical_fov = 2*atan(V_h/(2*d))
    right_plane = [-cos(horizontal_fov/2), 0, -sin(horizontal_fov/2)]
    left_plane = [cos(horizontal_fov/2), 0, -sin(horizontal_fov/2)]
    up_plane = [0, -cos(vertical_fov/2), -sin(vertical_fov/2)]
    down_plane = [0, cos(vertical_fov/2), -sin(vertical_fov/2)]
    planes = [right_plane, left_plane, up_plane, down_plane]
    for face in faces:
        if face[2][2] < zfar or face[2][2] > znear:
            continue
        for plane in planes:
            if dot(face[2], plane) < error:
                continue
            done.append(face)
    return done
    