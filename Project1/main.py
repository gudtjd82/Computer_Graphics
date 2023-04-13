from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np
from shader import load_shaders
from prepare_vao import *
from draw import *

g_cam_ang_x = 0.
g_cam_ang_y = 0.
g_cam_height = .1
eye_vec = glm.vec3(0, .1, .1)
center_vec = glm.vec3(0, 0, 0)
up_vec = glm.vec3(0,1,0)
view_mat = glm.lookAt(eye_vec, center_vec, up_vec)
mouse_x = 0
mouse_y = 0
mouse_click = 0     # 0=>none, 1=>left, 2=>right
mouse_press_x = 0
mouse_press_y = 0
mouse_release_x = 0
mouse_release_y = 0
pre_diff_x_1 = 0
pre_diff_y_1 = 0
diff_x_1 = 0
diff_y_1 = 0
pre_diff_x_2 = 0
pre_diff_y_2 = 0
diff_x_2 = 0
diff_y_2 = 0
pre_diff_x_3 = 0
pre_diff_y_3 = 0
diff_x_3 = 0
diff_y_3 = 0
click_V = 0

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
    global g_cam_ang_x, g_cam_height, click_V
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_1:
                g_cam_ang_x += np.radians(-10)
            elif key==GLFW_KEY_3:
                g_cam_ang_x += np.radians(10)
            elif key==GLFW_KEY_2:
                g_cam_height += .1
            elif key==GLFW_KEY_W:
                g_cam_height += -.1
            elif key==GLFW_KEY_V:
                click_V = 1;

#마우스 커서 움직임 이벤트 callback 함수
def cursor_callback(window, xpos, ypos):
    global mouse_x, mouse_y
    mouse_x = xpos
    mouse_y = ypos

#마우스 버튼 움직임 이벤트 callback 함수
def button_callback(window, button, action, mod):
    global mouse_x, mouse_y, mouse_press_x, mouse_press_y, mouse_click, diff_x_1, diff_y_1, diff_x_2, diff_y_2, pre_diff_x_1, pre_diff_y_1, pre_diff_x_2, pre_diff_y_2

    #Orbit
    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            mouse_click = 1     
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
            # print('press left btn: (%d, %d)' % (mouse_press_x, mouse_press_y))
        elif action == GLFW_RELEASE:
            mouse_click = 0
            pre_diff_x_1 = diff_x_1
            pre_diff_y_1 = diff_y_1

    #Pan
    elif button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            mouse_click = 2
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
            # print('press left btn: (%d, %d)' % (mouse_x, mouse_y))
        elif action == GLFW_RELEASE:
            mouse_click = 0
            pre_diff_x_2 = diff_x_2
            pre_diff_y_2 = diff_y_2
            # (mouse_release_x, mouse_release_y) = glfwGetCursorPos(window)
            # print('release left btn: (%d, %d)' % (mouse_release_x, mouse_release_y))
            
    else:
        mouse_click = 0

#마우스 스크롤 움직임 이벤트 callback 함수
def scroll_callback(window, xoffset, yoffset):
    global mouse_click, eye_vec
    mouse_click = 3
    print('mouse wheel scroll: %d, %d' % (xoffset, yoffset))

def cam_orbit():
    global diff_x_1, diff_y_1, g_cam_ang_x, g_cam_ang_y
    
    diff_x_1 = pre_diff_x_1 + mouse_press_x - mouse_x
    diff_y_1 = pre_diff_y_1 + mouse_press_y - mouse_y
    g_cam_ang_x = -np.radians(diff_x_1)
    g_cam_ang_y = -np.radians(diff_y_1)
    sensitive = 15
    g_cam_ang_x *= sensitive
    g_cam_ang_y *= sensitive
 
def cam_pan():
    global diff_x_2, diff_y_2, g_cam_ang_x, g_cam_height

    diff_x_2 = mouse_press_x - mouse_x
    diff_y_2 = mouse_press_y - mouse_y
    sensitive = 0.002
    diff_x_2 *= -sensitive
    diff_y_2 *= sensitive*2
    diff_x_2 += pre_diff_x_2
    diff_y_2 += pre_diff_y_2

def cam_zoom():
    global diff_x_3, diff_y_3

def update_view_mat():
    global view_mat

    #orbit
    R = glm.mat4(1.0)
    R = glm.rotate(R, glm.radians(g_cam_ang_y), glm.vec3(1,0,0))
    R = glm.rotate(R, glm.radians(g_cam_ang_x), glm.vec3(0,1,0))
    
    #pan
    T = glm.mat4(1.0)
    T = glm.translate(T, glm.vec3(diff_x_2, diff_y_2, 0))

    view_mat = glm.lookAt(eye_vec, center_vec, up_vec) * T * R

def main():
    global click_V, view_mat, eye_vec, center_vec, up_vec
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
    vao_cube = prepare_vao_cube()
    vao_frame = prepare_vao_frame()
    vao_grid_x = prepare_vao_grid_x()
    vao_grid_z = prepare_vao_grid_z()
    V = glm.lookAt(glm.vec3(0, .1, .1), glm.vec3(0,0,0), glm.vec3(0,1,0))

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

        

        #왼쪽 클릭 시에는(1) orbit, 오른쪽 클릭 시에는(2) pan, 휠 회전 시에는(3) zoom
        if mouse_click == 1:
            cam_orbit()
            update_view_mat()
      
        elif mouse_click == 2:
            cam_pan()
            update_view_mat()
            # change_x = diff_x_2/1000
            # change_y = diff_y_2/1000
            # eye_vec = glm.vec3(.1*np.sin(g_cam_ang_x) + change_x, g_cam_height + change_y,.1*np.cos(g_cam_ang_x) + change_x)
            # center_vec = glm.vec3(change_x, change_y, change_x)
            # V =glm.lookAt(eye_vec, center_vec, up_vec)
        
        elif mouse_click == 3:
            cam_zoom()
            update_view_mat()   
            V = glm.lookAt(eye_vec, center_vec, up_vec)

        V = view_mat
        
            

            # V = glm.lookAt(eye_vec, center_vec, up_vec)
            # print('difference right btn: (%d, %d)' % (diff_x_1, diff_y_1))


        # view matrix
        # rotate camera position with g_cam_ang_x / move camera up & down with g_cam_height
        
            # print('press left btn: (%d, %d)' % (mouse_x, mouse_press_y))
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
        T = glm.translate(glm.vec3(0, 0.1, 0))

        # scaling
        S = glm.scale(glm.vec3(np.sin(t), np.sin(t), np.sin(t)))

        # M = R
        M = T
        # M = S
        # M = R @ T
        # M = T @ R

        # current frame: P*V*M
        MVP = P*V*M
        if click_V == 1:
            print(V)
            click_V = 0
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        # draw triangle w.r.t. the current frame
        draw_cube(vao_cube, P*V*M, MVP_loc)

        #바닥(xz)에 격자
        draw_grid(vao_grid_x,vao_grid_z, P*V*glm.mat4(), MVP_loc)

        # draw current frame
        draw_frame(vao_frame, P*V*glm.mat4(), MVP_loc)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
