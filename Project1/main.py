from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np
from shader import load_shaders
from prepare_vao import *

g_cam_ang = 0.
g_cam_height = .1
seq = 1    # +1 or -1   
mouse_x_0 = 0
mouse_y_0 = 0
mouse_x_1 = 0
mouse_y_1 = 0
mouse_click = 0     # 0=>none, 1=>left, 2=>right
mouse_press_x = 0
mouse_press_y = 0
# mouse_z = 0
mouse_release_x = 0
mouse_release_y = 0
# mouse_click_z = 0;
pre_mouse_diff_x = 0
pre_mouse_diff_y = 0
mouse_diff_x = 0
mouse_diff_y = 0

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
    global g_cam_ang, g_cam_height
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_1:
                g_cam_ang += np.radians(-10)
            elif key==GLFW_KEY_3:
                g_cam_ang += np.radians(10)
            elif key==GLFW_KEY_2:
                g_cam_height += .1
            elif key==GLFW_KEY_W:
                g_cam_height += -.1

#마우스 커서 움직임 이벤트 callback 함수
def cursor_callback(window, xpos, ypos):
    global mouse_x_0, mouse_y_0, mouse_x_1, mouse_y_1, seq
    # if seq == 1:
    #     mouse_x_0 = xpos
    #     mouse_y_0 = ypos
    # elif seq == -1:
    #     mouse_x_1 = xpos
    #     mouse_y_1 = ypos
    mouse_x_0 = xpos
    mouse_y_0 = ypos
#     global mouse_press_x, mouse_press_y
    
#     # mouse_z = zposz
    # print("(%d, %d)" %(mouse_x, mouse_y))

#마우스 버튼 움직임 이벤트 callback 함수
def button_callback(window, button, action, mod):
    global mouse_x_0, mouse_y_0,mouse_press_x, mouse_press_y, mouse_release_x, mouse_release_y, mouse_click, mouse_diff_x, mouse_diff_y, g_cam_ang, g_cam_height, pre_mouse_diff_x, pre_mouse_diff_y

    #Orbit
    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            # seq *= -1
            mouse_click = 1     
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
            print('press left btn: (%d, %d)' % (mouse_press_x, mouse_press_y))
        elif action == GLFW_RELEASE:
            mouse_click = 0
            pre_mouse_diff_x = mouse_diff_x
            pre_mouse_diff_y = mouse_diff_y
            # init_mouse()
            # (mouse_release_x, mouse_release_y) = glfwGetCursorPos(window)
            # print('press left btn: (%d, %d)' % (mouse_x_0, mouse_y_0))
            # print('release left btn: (%d, %d)' % (mouse_release_x, mouse_release_y))
            # mouse_diff_x = mouse_x_0 - mouse_release_x
            # mouse_diff_y = mouse_y_0 - mouse_release_y
            # print('difference left btn: (%d, %d)' % (mouse_diff_x, mouse_diff_y))
            # g_cam_ang += np.radians(mouse_diff_x/10)
            # g_cam_height += mouse_diff_y/100
    #Pan
    elif button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            mouse_click = 2
            (mouse_x_0, mouse_y_0) = glfwGetCursorPos(window)
            seq = 1
            print('press left btn: (%d, %d)' % (mouse_x_0, mouse_y_0))
        elif action == GLFW_RELEASE:
            mouse_click = 0
            (mouse_release_x, mouse_release_y) = glfwGetCursorPos(window)
            seq = 0
            init_mouse()
            print('release left btn: (%d, %d)' % (mouse_release_x, mouse_release_y))
            
    else:
        mouse_click = 0

#마우스 스크롤 움직임 이벤트 callback 함수
def scroll_callback(window, xoffset, yoffset):
    print('mouse wheel scroll: %d, %d' % (xoffset, yoffset))

def init_mouse():
    global mouse_x_0, mouse_x_1, mouse_y_0, mouse_y_1
    mouse_x_0 = 0
    mouse_x_1 = 0
    mouse_y_0 = 0
    mouse_y_1 = 0

def cam_orbit():
    global mouse_diff_x, mouse_diff_y, g_cam_ang, g_cam_height, seq
    
    # print('mouse position: (%d, %d)' % (mouse_x, mouse_y))
    #azimuth
    mouse_diff_x = pre_mouse_diff_x + mouse_press_x - mouse_x_0
    g_cam_ang = np.radians(mouse_diff_x/10)

    #elevation
    mouse_diff_y = pre_mouse_diff_y + mouse_press_y - mouse_y_0
    g_cam_height = 0.1 + -mouse_diff_y/1000
    print('difference left btn: (%d, %d)' % (mouse_diff_x, mouse_diff_y))
    
 
def cam_pan():
    global mouse_diff_x, mouse_diff_y, g_cam_ang, g_cam_height

def main():
    global mouse_click, seq, seq
    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(800, 800, '3-lookat', None, None)
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
    vao_triangle = prepare_vao_triangle()
    vao_frame = prepare_vao_frame()

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # render

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glUseProgram(shader_program)

        # projection matrix
        # use orthogonal projection (we'll see details later)
        P = glm.ortho(-1,1,-1,1,-1,1)

        # view matrix
        # rotate camera position with g_cam_ang / move camera up & down with g_cam_height
        if mouse_click == 1:
            cam_orbit()
            # print('difference left btn: (%d, %d)' % (mouse_diff_x, mouse_diff_y))
        elif mouse_click == 2:
            cam_pan()
            # print('difference right btn: (%d, %d)' % (mouse_diff_x, mouse_diff_y))

        up_vec = glm.vec3(0,1,0)
        center_vec = glm.vec3(0, 0, 0)

        V = glm.lookAt(glm.vec3(.1*np.sin(g_cam_ang),g_cam_height,.1*np.cos(g_cam_ang)), center_vec, up_vec)
        # V = glm.lookAt(glm.vec3(0.1 , 0.1, 0.1), glm.vec3(0,0,0), glm.vec3(0,1,0))
            # print('press left btn: (%d, %d)' % (mouse_x_0, mouse_press_y))
            # print('release left btn: (%d, %d)' % (mouse_release_x, mouse_release_y))
            

            # print('press left btn: (%d, %d)' % (mouse_press_x, mouse_press_y))
            # print('release left btn: (%d, %d)' % (mouse_release_x, mouse_release_y))


        # current frame: P*V*I (now this is the world frame)
        I = glm.mat4()
        MVP = P*V*I
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        # draw current frame
        glBindVertexArray(vao_frame)
        glDrawArrays(GL_LINES, 0, 6)


        # animating
        t = glfwGetTime()

        # rotation
        th = np.radians(t*90)
        R = glm.rotate(th, glm.vec3(0,0,1))

        # tranlation
        T = glm.translate(glm.vec3(0, 0, 0.))

        # scaling
        S = glm.scale(glm.vec3(np.sin(t), np.sin(t), np.sin(t)))

        # M = R
        M = T
        # M = S
        # M = R @ T
        # M = T @ R

        # current frame: P*V*M
        MVP = P*V*M
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        # draw triangle w.r.t. the current frame
        glBindVertexArray(vao_triangle)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # draw current frame
        glBindVertexArray(vao_frame)
        glDrawArrays(GL_LINES, 0, 6)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
