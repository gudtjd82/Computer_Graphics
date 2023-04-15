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
distance = 5

#for lookat function
eye_vec = glm.vec3(np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)), np.sin(np.radians(elevation)), np.cos(np.radians(elevation))*np.cos(np.radians(azimuth))) * distance
center_vec = glm.vec3(0, 0, 0)
up_vec = glm.vec3(0,1,0)    # v axis of camera        

#camera frame
front_vec = glm.normalize(eye_vec - center_vec)         # W axis of camera
right_vec = glm.normalize(glm.cross(up_vec, front_vec)) # u axis of camera
v_vec = glm.normalize(glm.cross(front_vec, right_vec))  # v axis of camera

#기타 변수
mouse_x = 0
mouse_y = 0
mouse_click = 0     # 0=>none, 1=>left, 2=>right
mouse_press_x = 0
mouse_press_y = 0
diff_x_1 = 0
diff_y_1 = 0
diff_x_2 = 0
diff_y_2 = 0
move_x = 0
move_y = 0
scroll = 0
click_V = 1

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
}
'''

#키보드 눌림 이벤트 callback 함수
def key_callback(window, key, scancode, action, mods):
    global pitch, g_cam_height, click_V, click_C
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_V:
                click_V *= -1

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
    global mouse_click, scroll, eye_vec, front_vec
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
    
    scroll = 0 

# updating view_mat
def update_view_mat():
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
   
def main():

    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(800, 800, '202104242 박성현', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);
    glfwSetCursorPosCallback(window, cursor_callback) 
    glfwSetMouseButtonCallback(window, button_callback)
    glfwSetScrollCallback(window, scroll_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
     
    # prepare vaos
    vao_cube = prepare_vao_cube()
    vao_frame = prepare_vao_frame()
    vao_grid_x = prepare_vao_grid_x()
    vao_grid_z = prepare_vao_grid_z()

    

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glUseProgram(shader_program)

        #projection / orthogonal
        orth = 5
        if click_V == 1:
            P = glm.perspective(45, 1, .1, 100)
        elif click_V == -1:
            P = glm.ortho(-orth,orth,-orth,orth, .1, 100)

        update_view_mat()

        V = glm.lookAt(eye_vec, center_vec, up_vec)
        
        M = glm.mat4()
        # draw frame
        draw_frame(vao_frame, P*V*M, MVP_loc)

        MVP = P*V*M

        #바닥(xz)에 격자
        draw_grid(vao_grid_x,vao_grid_z, P*V*glm.mat4(), MVP_loc)

        # draw cube
        draw_cube(vao_cube, P*V*M, MVP_loc)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
