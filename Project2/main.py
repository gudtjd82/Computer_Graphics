from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np
from shader import load_shaders
from prepare_vao import *
from draw import *
from node import *
from obj import *
from animation import *
import os


# camera 각도, 거리
azimuth = 45
elevation = 45
distance = 30

#for lookat function
eye_vec = glm.vec3(
    np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)), 
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

# mode 관련 변수 - 키보드 특정 키 클릭 유무
click_V = 1         
click_H = 1
click_Z = 1

# drop obj file 관련 변수
drop_path = ""       # dropp된 file path
drop_OBJ = Obj("")   # drop된 file의 obj 객체

# drop 관련 bool 변수
first_drop = False  # file이 drop되고 처음 도는 loop인지 확인
file_drop = False   # drop된 file이 존재하는지 확인

# Hierarchical model redering mode
# Hierarchical objs
casino_path = os.path.join(".", "Casino")                               # hierarchical model obj file이 저장된 폴더 위치
unif_objs = {}
unif_objs["table"] = Obj(os.path.join(casino_path, "Casino_Table.obj"))   # Casino Table obj 객체
unif_objs["spade"] = Obj(os.path.join(casino_path, "Spade_Card.obj"))            # Spade Card obj 객체
unif_objs["dia"] = Obj(os.path.join(casino_path, "Diamond_Card.obj"))        # Diamod Card obj 객체
unif_objs["heart"] = Obj(os.path.join(casino_path, "Heart_Card.obj"))            # Heart Card obj 객체
unif_objs["clover"] = Obj(os.path.join(casino_path, "Clover_Card.obj"))          # Clover Card obj 객체
unif_objs["chip"] = Obj(os.path.join(casino_path, "Chip.obj"))                   # Chip obj 객체

# Vertex Shader for frame
g_vertex_shader_src_color_attribute = '''
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

# Fragment Shader for frame
g_fragment_shader_src = '''
#version 330 core

in vec4 vout_color;

out vec4 FragColor;

void main()
{
    FragColor = vout_color;
}
'''

# Vertex Shader for lighting mode
g_vertex_shader_src_lighting = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_normal; 

out vec3 vout_surface_pos;
out vec3 vout_normal;
out vec3 vout_color;

uniform mat4 MVP;
uniform mat4 M;
uniform vec3 color;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);
    gl_Position = MVP * p3D_in_hcoord;

    vout_surface_pos = vec3(M * vec4(vin_pos, 1));
    vout_normal = normalize( mat3(inverse(transpose(M)) ) * vin_normal);
    vout_color = color;

}
'''

# Fragment Shader for lighting mode
g_fragment_shader_src_lighting = '''
#version 330 core

in vec3 vout_surface_pos;
in vec3 vout_normal;
in vec3 vout_color;

out vec4 FragColor;

uniform vec3 view_pos;
//uniform mat4 light_rotate;

void main()
{
    // light and material properties
    //vec3 light_pos = vec3(light_rotate * vec4(2, 2, 0, 1));
    //vec3 light_pos = vec3(3,2,4);
    vec3 light_pos = vec3(0,12,0);
    vec3 light_color = vec3(1,1,1);
    vec3 material_color = vout_color;
    float material_shininess = 32.0;

    // light components
    vec3 light_ambient = 0.1*light_color;
    vec3 light_diffuse = light_color;
    vec3 light_specular = light_color;

    // material components
    vec3 material_ambient = material_color;
    vec3 material_diffuse = material_color;
    vec3 material_specular = light_color;  // for non-metal material

    // ambient
    vec3 ambient = light_ambient * material_ambient;

    // for diffiuse and specular
    vec3 normal = normalize(vout_normal);
    vec3 surface_pos = vout_surface_pos;
    vec3 light_dir = normalize(light_pos - surface_pos);

    // diffuse
    float diff = max(dot(normal, light_dir), 0);
    vec3 diffuse = diff * light_diffuse * material_diffuse;

    // specular
    vec3 view_dir = normalize(view_pos - surface_pos);
    vec3 reflect_dir = reflect(-light_dir, normal);
    float spec = pow( max(dot(view_dir, reflect_dir), 0.0), material_shininess);
    vec3 specular = spec * light_specular * material_specular;

    vec3 color = ambient + diffuse + specular;
    FragColor = vec4(color, 1.);
}
'''


#키보드 눌림 이벤트 callback 함수
def key_callback(window, key, scancode, action, mods):
    global click_V, click_H, file_drop, click_Z
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_V:
                click_V *= -1
            elif key==GLFW_KEY_H:
                click_H *= -1
                # if click_H == -1:
                #     file_drop = False
            elif key==GLFW_KEY_Z:
                click_Z *= -1

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
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
            mouse_click = 0
            
    #Pan
    elif button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            mouse_click = 2
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
        elif action == GLFW_RELEASE:
            (mouse_press_x, mouse_press_y) = glfwGetCursorPos(window)
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
    if(move_x != 0 and mouse_y != 0):
        move_x = diff_x_2 * right_vec * -sensitivity
        move_y = diff_y_2 * v_vec * sensitivity
    else:
        move_x = glm.vec3(0,0,0)
        move_y = glm.vec3(0,0,0)
    
    eye_vec += move_x + move_y
    center_vec += move_x + move_y
    mouse_press_x = mouse_x
    mouse_press_y = mouse_y

#camera zooming
def cam_zoom():
    global scroll, distance

    sensitivity = 0.05 * distance

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
        # print("elevation: ", elevation)
        # print("azimuth: ", azimuth)
        eye_vec = glm.vec3(np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)), np.sin(np.radians(elevation)), np.cos(np.radians(elevation))*np.cos(np.radians(azimuth))) * distance
        # print("eye_pos in cam_orbit 1: \n", eye_vec)
        # print("----------------------------")
        eye_vec += center_vec

        # print("eye_pos in cam_orbit 2: \n", eye_vec)
        # print("----------------------------")

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
    global drop_path, first_drop, file_drop, click_H

    # 기존의 Obj 관련 변수 초기화
    # initOBJ()
    file_drop = False
    drop_OBJ.__init__("")

    # for path in paths:
    # drop_path = os.path.join(os.getcwd(), paths[0])
    drop_path = paths[0]
    first_drop = True
    file_drop = True
    click_H = 1

    # paths 초기화
    paths.__init__()

def main():
    global first_drop, click_H

    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(1000, 1000, '202104242 박성현', None, None)
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
    shader_for_frame = load_shaders(g_vertex_shader_src_color_attribute, g_fragment_shader_src)
    shader_for_lighting = load_shaders(g_vertex_shader_src_lighting, g_fragment_shader_src_lighting)

    # get uniform locations
    MVP_loc_frame = glGetUniformLocation(shader_for_frame, 'MVP')
    loc_names = ['MVP', 'M', 'view_pos', 'color']
    unif_locs = {}
    for name in loc_names:
        unif_locs[name] = glGetUniformLocation(shader_for_lighting, name)
     
    # create Casino nodes
    unif_nodes = {}
    size_of_table = 1
    size_of_card = 0.9
    size_of_chip = 0.7
    scale_table = glm.scale((size_of_table,size_of_table,size_of_table))
    scale_card = glm.scale((size_of_card,size_of_card,size_of_card))
    scale_chip = glm.scale((size_of_chip,size_of_chip,size_of_chip))
    unif_nodes["table"] = Node(None, scale_table, glm.vec3(0.70196, 0.23922, 0.23922))
    unif_nodes["spade"] = Node(unif_nodes["table"], scale_card, glm.vec3(0.69020, 0.29804, 0.78039))
    unif_nodes["dia"] = Node(unif_nodes["table"], scale_card, glm.vec3(0.26275, 0.65882, 0.70980))
    unif_nodes["heart"] = Node(unif_nodes["table"], scale_card, glm.vec3(0.87059, 0.31373, 0.50980))
    unif_nodes["clover"] = Node(unif_nodes["table"], scale_card, glm.vec3(0.32941, 0.72157, 0.36863))
    unif_nodes["chip_of_H"] = Node(unif_nodes["heart"], scale_chip, glm.vec3(0.87059, 0.83529, 0.20000))
    unif_nodes["chip_of_C"] = Node(unif_nodes["clover"], scale_chip, glm.vec3(0.25882, 0.36863, 0.81176))

    # prepare vaos      
    unif_vaos = {}
    unif_vaos["vao_frame"] = prepare_vao_frame()
    unif_vaos["vao_grid_x"] = prepare_vao_grid_x()
    unif_vaos["vao_grid_z"] = prepare_vao_grid_z()
    unif_vaos["vao_drop_obj"] = prepare_vao_obj(Obj(""))
    # prepare casino node vaos
    unif_vaos["table"] = prepare_vao_obj(unif_objs["table"])
    unif_vaos["spade"] = prepare_vao_obj(unif_objs["spade"])
    unif_vaos["dia"] = prepare_vao_obj(unif_objs["dia"])
    unif_vaos["heart"] = prepare_vao_obj(unif_objs["heart"])
    unif_vaos["clover"] = prepare_vao_obj(unif_objs["clover"])
    unif_vaos["chip"] = prepare_vao_obj(unif_objs["chip"])

    # animation을 위한 현재 time 변수
    start_time = glfwGetTime()
    start_time2 = glfwGetTime()
    start_time3 = glfwGetTime()

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # wireframe / solid mode
        if click_Z == -1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif click_Z == 1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # projection / orthogonal
        ortho = 5
        if click_V == 1:
            P = glm.perspective(45, 1, .1, 1000)
        elif click_V == -1:
            P = glm.ortho(-ortho, ortho, -ortho, ortho, .1, 1000)

        update_vec()

        V = glm.lookAt(eye_vec, center_vec, up_vec)
        
        M = glm.mat4()

        MVP = P*V*M

        # draw frame
        glUseProgram(shader_for_frame)
        draw_frame(unif_vaos["vao_frame"], MVP, MVP_loc_frame)

        # 바닥(xz)에 격자
        draw_grid(unif_vaos["vao_grid_x"],unif_vaos["vao_grid_z"], MVP, MVP_loc_frame)

        glUseProgram(shader_for_lighting)
        glUniform3f(unif_locs["view_pos"], eye_vec.x, eye_vec.y, eye_vec.z)
        glUniform3f(unif_locs["color"], 0, 0.4, 0.1)

        # obj파일이 처음 drop되었을 때
        if first_drop:
            drop_OBJ.set_path(drop_path)
            
            drop_OBJ.display_objInfo()

            unif_vaos["vao_drop_obj"] = prepare_vao_obj(drop_OBJ)

            first_drop = False
        
        glUniformMatrix4fv(unif_locs["M"], 1, GL_FALSE, glm.value_ptr(M))

        if click_H == 1:
            num_of_vertices = drop_OBJ.get_num_of_vertices()

            # draw dropped obj
            draw_obj(unif_vaos["vao_drop_obj"], MVP, unif_locs["MVP"], num_of_vertices)

        if click_H == -1:
            VP = P*V

            # time value for animating
            t = glfwGetTime()
            speed = 3
            spread = 15 
            th = np.radians(spread*np.sin(t*speed) +spread)

            # draw Table
            draw_node(unif_vaos["table"], unif_nodes["table"], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["table"])

            # Animation 1 - User1: spade, heart, dia, chip1-10
            pos1 = glm.vec3(7.5,7.18,3.5)
            cards1 = ["spade", "heart", "dia"]
            animation_cardSpread(unif_locs, unif_vaos, unif_nodes, unif_objs, cards1, VP, pos1, th)
            # chip suffling animation
            m = glfwGetTime() - start_time  # 시간의 흐름
            unit = 0.6                      # 동작의 시간 단위
            x_pos = -3.5                    # 부모 노드로부터의 chip의 x 위치
            temp_time = animation_chipShuffle(unif_locs, unif_vaos, unif_nodes, unif_objs, "chip_of_H", VP, m, start_time, unit, x_pos, th, +1)
            if temp_time != None :
                start_time = temp_time
            

            # Animation 2 - User2: dia, clover, heart, chip11-20
            pos2 = glm.vec3(-7.5,7.18,3.5)
            cards2 = ["dia", "clover", "heart"]
            animation_cardSpread(unif_locs, unif_vaos, unif_nodes, unif_objs, cards2, VP, pos2, -th)
            # chip suffling animation
            m = glfwGetTime() - start_time2  # 시간의 흐름
            unit = 0.6                      # 동작의 시간 단위
            x_pos = 3.5                    # 부모 노드로부터의 chip의 x 위치
            temp_time2 = animation_chipShuffle(unif_locs, unif_vaos, unif_nodes, unif_objs, "chip_of_C", VP, m, start_time2, unit, x_pos, th, -1)
            if  temp_time2 != None:
                start_time2 = temp_time2


            # Animation 3 - show down 4 cards - spade, dia, heart, clover
            unit = 0.5                          # animation 동장 단위
            m = glfwGetTime() - start_time3     # 시간의 흐름
            size = 0.7                          # card size 
            S = glm.scale((size, size, size))   # card size scale
            T = glm.translate((-0.5,0,0))         
            ST = T * S
            temp_time3 = animation_showDown(unif_locs, unif_vaos, unif_nodes, unif_objs, VP, m, start_time3, unit, ST)
            if  temp_time3 != None:
                start_time3 = temp_time3

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
