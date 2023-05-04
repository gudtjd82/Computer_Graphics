from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np
from shader import load_shaders
from prepare_vao import *
from draw import *

# camera 각도, 거리
azimuth = 45
elevation = 45
distance = 10

#for lookat function
eye_vec = glm.vec3(np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)), 
                    np.sin(np.radians(elevation)), 
                    np.cos(np.radians(elevation))*np.cos(np.radians(azimuth))) * distance
center_vec = glm.vec3(0, 0, 0)
up_vec = glm.vec3(0,1,0)    # v axis of camera        

#camera frame
front_vec = glm.normalize(eye_vec - center_vec)         # W axis of camera
right_vec = glm.normalize(glm.cross(up_vec, front_vec)) # u axis of camera
v_vec = glm.normalize(glm.cross(front_vec, right_vec))  # v axis of camera

# cam 관련 기타 변수
mouse_x = 0
mouse_y = 0
mouse_click = 0     # 0=>none, 1=>left, 2=>right, 3=>wheel
mouse_press_x = 0
mouse_press_y = 0
diff_x_1 = 0        # orbit에서 사용
diff_y_1 = 0        # orbit에서 사용
diff_x_2 = 0        # pan에서 사용
diff_y_2 = 0        # pan에서 사용
move_x = 0          # pan에서 사용
move_y = 0          # pan에서 사용
scroll = 0          # zoom에서 사용
click_V = 1         

# obj file 관련 변수
obj_path = ""       # dropped file path
pVertices = []      # vertex position array
nVertices = []      # vertex normal array
faces_3v = []       # face with 3 vertices
faces_4v = []       # face with 4 vertices
faces_more = []     # face with 5+ vertices
first_drop = False  # file이 드롭되고 처음 도는 loop인지 확인
file_drop = False   # file이 드롭된 상태인지 체크
click_H = 1

g_vertex_shader_src = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_color; 

out vec4 vout_color;

uniform mat4 MVP;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);

    gl_Position = MVP * p3D_in_hcoord;

    vout_color = vec4(vin_color, 1.);
}
'''

g_fragment_shader_src = '''
#version 330 core

in vec4 vout_color;

out vec4 FragColor;

void main()
{
    FragColor = vout_color;
    //FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f)
}
'''

# Node 객체
class Node:
    def __init__(self, parent, shape_transform, color):
        # hierarchy
        self.parent = parent
        self.children = []
        if parent is not None:
            parent.children.append(self)

        # transform
        self.transform = glm.mat4()
        self.global_transform = glm.mat4()

        # shape
        self.shape_transform = shape_transform
        self.color = color

    def set_transform(self, transform):
        self.transform = transform

    def update_tree_global_transform(self):
        if self.parent is not None:
            self.global_transform = self.parent.get_global_transform() * self.transform
        else:
            self.global_transform = self.transform

        for child in self.children:
            child.update_tree_global_transform()

    def get_global_transform(self):
        return self.global_transform
    def get_shape_transform(self):
        return self.shape_transform
    def get_color(self):
        return self.color

#키보드 눌림 이벤트 callback 함수
def key_callback(window, key, scancode, action, mods):
    global click_V, click_H
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_V:
                click_V *= -1
            elif key==GLFW_KEY_H:
                click_H *= -1

#마우스 커서 움직임 이벤트 callback 함수
def cursor_callback(window, xpos, ypos):
    global mouse_x, mouse_y
    mouse_x = xpos
    mouse_y = ypos

#마우스 버튼 움직임 이벤트 callback 함수
def button_callback(window, button, action, mod):
    global mouse_press_x, mouse_press_y, mouse_click

    #Orbit
    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            mouse_click = 1     
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
        elif action == GLFW_RELEASE:
            mouse_click = 0
            
    #Pan
    elif button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            mouse_click = 2
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
        elif action == GLFW_RELEASE:
            mouse_click = 0

#마우스 스크롤 움직임 이벤트 callback 함수
def scroll_callback(window, xoffset, yoffset):
    global mouse_click, scroll
    mouse_click = 3
    scroll = yoffset

#camera oribit
def cam_orbit():
    global diff_x_1, diff_y_1, mouse_press_x, mouse_press_y, azimuth, elevation, front_vec, v_vec, right_vec, up_vec
    
    diff_x_1 = mouse_press_x - mouse_x
    diff_y_1 = mouse_press_y - mouse_y
    mouse_press_x = mouse_x
    mouse_press_y = mouse_y

    vertical_sensitivity = .17
    horizontal_sensitivity = .15
    elevation += diff_y_1 * - vertical_sensitivity

    quard =  elevation/90 % 4
    reverse = 1
    if 0 < quard < 1 or quard >= 3:
        up_vec = glm.vec3(0, +1, 0)
        reverse = 1
    elif 1 <= quard < 3:
        up_vec  = glm.vec3(0, -1, 0)
        reverse = -1

    azimuth += diff_x_1 * horizontal_sensitivity * reverse

    right_vec = glm.rotate(right_vec, np.radians(elevation), glm.cross(glm.vec3(0,1,0), -front_vec))
    right_vec = glm.rotate(right_vec, np.radians(azimuth), glm.vec3(0,1,0))
    v_vec = glm.rotate(v_vec, np.radians(elevation), glm.cross(glm.vec3(0,1,0), -front_vec))
    v_vec = glm.rotate(v_vec, np.radians(azimuth), glm.vec3(0,1,0))
    front_vec = glm.rotate(front_vec, np.radians(elevation), glm.cross(glm.vec3(0,1,0), -front_vec))
    front_vec = glm.rotate(front_vec, np.radians(azimuth), glm.vec3(0,1,0))

#camera panning
def cam_pan():
    global diff_x_2, diff_y_2, eye_vec, center_vec, mouse_x, mouse_y, mouse_press_x,mouse_press_y, move_x, move_y

    diff_x_2 =mouse_x - mouse_press_x
    diff_y_2 = mouse_y - mouse_press_y

    sensitivity = 0.0008 * distance
    move_x = diff_x_2 * right_vec * -sensitivity
    move_y = diff_y_2 * v_vec * sensitivity
    
    eye_vec += move_x + move_y
    center_vec += move_x + move_y
    
    mouse_press_x = mouse_x
    mouse_press_y = mouse_y

#camera zooming
def cam_zoom():
    global scroll, distance

    sensitivity = 0.5

    if scroll > 0:
        distance -= sensitivity
        scroll -= 1

    elif scroll < 0:
        distance += sensitivity
        scroll += 1
    
    if distance <= 0.1:
        distance = 0.1

    scroll = 0 

# updating vectors
def update_vec():
    global view_mat, eye_vec, front_vec, right_vec, v_vec
    
    #orbit
    if mouse_click == 1:
        cam_orbit()
        eye_vec = glm.vec3(np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)), np.sin(np.radians(elevation)), np.cos(np.radians(elevation))*np.cos(np.radians(azimuth))) * distance
        eye_vec += center_vec

    #pan
    elif mouse_click == 2:
        cam_pan()
        front_vec = glm.normalize(eye_vec - center_vec)   # W axis of camera
        right_vec = glm.normalize(glm.cross(up_vec, front_vec)) # u axis of camera
        v_vec = glm.normalize(glm.cross(front_vec, right_vec))  # v axis of camera

    #zoom
    elif mouse_click == 3:
        cam_zoom()
        eye_vec = glm.vec3(np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)), np.sin(np.radians(elevation)), np.cos(np.radians(elevation))*np.cos(np.radians(azimuth))) * distance
        eye_vec += center_vec

# file drop callback function
def drop_callback(window, paths):
    global obj_path, first_drop, file_drop

    print("drop_callback call")

    # 기존의 Obj 관련 변수 초기화
    initOBJ()

    # for path in paths:
    obj_path = paths[0]
    first_drop = True
    file_drop = True

    # paths 초기화
    paths.__init__()

# obj file을 parsing -> vertex와 face를 배열에 저장
def obj_parser(path, pVertices, nVertices, faces_3v, faces_4v, faces_more):
    with open(path, 'r') as file:
        lines = file.readlines()

    i = 0;
    for line in lines:
        tockens = line.strip().split()
        if len(tockens) > 0:
            if tockens[0] == "v":
                vertex = [float(v) for v in tockens[1:]]
                # print(i , "번째: ")
                # print(vertex)
                # print()
                pVertices.append(vertex)
            
            elif tockens[0] == "vn":
                vertex = [float(vn) for vn in tockens[1:]]
                nVertices.append(vertex)
            
            elif tockens[0] == "f":
                face = []
                for x in tockens[1:]:
                    i_str = x.strip().split("/")
                    i_int = [int(i_str[0]) - 1, int(i_str[2]) - 1]
                    face.append(i_int)
                if(len(face) == 3):
                    faces_3v.append(face)
                elif(len(face) == 4):
                    faces_4v.append(face)
                elif(len(face) > 4):
                    faces_more.append(face)
    # print("vertex position: \n", pVertices)
    # print("face_3v: \n", faces_3v)
    # print("\nface_4v: \n", faces_4v)


def initOBJ():
    global obj_path, pVertices, nVertices, faces_3v, faces_4v, faces_more, file_drop

    obj_path.__init__()
    pVertices.__init__()
    nVertices.__init__()
    faces_3v.__init__()
    faces_4v.__init__()
    faces_more.__init__()
    file_drop = False

def display_objInfo(fileName):
    num_of_faces = len(faces_3v)+len(faces_4v)

    print()
    print("------------------------------------------------")
    print("OBJ File Name:", fileName)
    print("Total Number of Faces:", num_of_faces)
    print("Number of Faces with 3 Vertices:", len(faces_3v))
    print("Number of Faces with 4 Vertices:", len(faces_4v))
    print("Number of Faces with 5+ Vertices:", len(faces_more))
    print("------------------------------------------------")
    print()

def single_mesh_mode(vao, MVP, MVP_loc):
    num_of_vertices = len(faces_3v)*3 + len(faces_4v)*2*3
    draw_obj(vao, MVP, MVP_loc, num_of_vertices) 

def main():
    global first_drop, g_P

    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(1500, 1500, '202104242 박성현', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback)
    glfwSetCursorPosCallback(window, cursor_callback) 
    glfwSetMouseButtonCallback(window, button_callback)
    glfwSetScrollCallback(window, scroll_callback)
    glfwSetDropCallback(window, drop_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
     
    # prepare vaos
    vao_cube = prepare_vao_cube()
    vao_frame = prepare_vao_frame()
    vao_grid_x = prepare_vao_grid_x()
    vao_grid_z = prepare_vao_grid_z()
    vao_obj = prepare_vao_obj(pVertices, nVertices, faces_3v, faces_4v, faces_more)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glUseProgram(shader_program)

        

        #projection / orthogonal
        ortho = 5
        if click_V == 1:
            P = glm.perspective(45, 1, .1, 100)
        elif click_V == -1:
            P = glm.ortho(-ortho, ortho, -ortho, ortho, .1, 100)

        update_vec()

        V = glm.lookAt(eye_vec, center_vec, up_vec)
        
        M = glm.mat4()

        MVP = P*V*M

        # draw frame
        draw_frame(vao_frame, MVP, MVP_loc)

        #바닥(xz)에 격자
        draw_grid(vao_grid_x,vao_grid_z, MVP, MVP_loc)

        # obj파일이 처음 drop되었을 때
        if first_drop:
            obj_parser(obj_path, pVertices, nVertices, faces_3v, faces_4v, faces_more)

            fileName = obj_path.strip().split("/").pop()
            display_objInfo(fileName)

            vao_obj = prepare_vao_obj(pVertices, nVertices, faces_3v, faces_4v, faces_more)

            first_drop = False
        
        # animating
        t = glfwGetTime()

        # rotation
        th = np.radians(t*90)
        M = glm.translate(glm.vec3(0, 0 , np.sin(th/3) * 10))

        MVP = P*V*M

        single_mesh_mode(vao_obj, MVP, MVP_loc)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
