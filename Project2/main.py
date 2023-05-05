from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np
from shader import load_shaders
from prepare_vao import *
from draw import *
from node import *
from obj import *
import os


# camera 각도, 거리
azimuth = 45
elevation = 45
distance = 50

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
click_V = 1         

# obj file 관련 변수
drop_path = ""       # dropped file path
drop_OBJ = Obj("")
# pVertices = []      # vertex position array
# nVertices = []      # vertex normal array
# faces_3v = []       # face with 3 vertices
# faces_4v = []       # face with 4 vertices
# faces_more = []     # face with 5+ vertices

# drop 관련 변수
first_drop = False  # file이 드롭되고 처음 도는 loop인지 확인
file_drop = False   # file이 드롭된 상태인지 체크
click_H = 1

# Hierarchical model redering mode
# Hierarchical objs
current_dir = os.getcwd()
casino_path = os.path.join(current_dir, "Casino")
Casino_table_obj = Obj(os.path.join(casino_path, "Casino_Table.obj"))
Clover_card_obj = Obj(os.path.join(casino_path, "Clover_Card.obj"))
Diamond_card_obj = Obj(os.path.join(casino_path, "Diamond_Card.obj"))
Heart_card_obj = Obj(os.path.join(casino_path, "Heart_Card.obj"))
Spade_card_obj = Obj(os.path.join(casino_path, "Spade_Card.obj"))
Chip_obj = Obj(os.path.join(casino_path, "Chip.obj"))

# single mesh mode & hierarchical mode
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

g_vertex_shader_src_color_uniform = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 

out vec4 vout_color;

uniform mat4 MVP;
uniform vec3 color;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);

    gl_Position = MVP * p3D_in_hcoord;

    vout_color = vec4(color, 1.);
    //vout_color = vec4(1,1,1,1);
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

# lighting mode
g_vertex_shader_src_lighting = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_normal; 

out vec3 vout_surface_pos;
out vec3 vout_normal;

uniform mat4 MVP;
uniform mat4 M;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);
    gl_Position = MVP * p3D_in_hcoord;

    vout_surface_pos = vec3(M * vec4(vin_pos, 1));
    vout_normal = normalize( mat3(inverse(transpose(M)) ) * vin_normal);

}
'''

g_fragment_shader_src_lighting = '''
#version 330 core

in vec3 vout_surface_pos;
in vec3 vout_normal;

out vec4 FragColor;

uniform vec3 view_pos;
uniform vec3 color;
//uniform mat4 light_rotate;

void main()
{
    // light and material properties
    //vec3 light_pos = vec3(light_rotate * vec4(2, 2, 0, 1));
    //vec3 light_pos = vec3(3,2,4);
    vec3 light_pos = vec3(0,10,0);
    vec3 light_color = vec3(1,1,1);
    vec3 material_color = color;
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
    global drop_path, first_drop, file_drop

    # 기존의 Obj 관련 변수 초기화
    # initOBJ()
    file_drop = False
    drop_OBJ.__init__("")

    # for path in paths:
    # drop_path = os.path.join(os.getcwd(), paths[0])
    drop_path = paths[0]
    print("path: ", drop_path)
    first_drop = True
    file_drop = True

    # paths 초기화
    paths.__init__()

def initOBJ():
    global drop_path, pVertices, nVertices, faces_3v, faces_4v, faces_more, file_drop

    drop_path.__init__()
    pVertices.__init__()
    nVertices.__init__()
    faces_3v.__init__()
    faces_4v.__init__()
    faces_more.__init__()
    file_drop = False


# 부모 노드가 parent인 num 개수만큼의 chip node 배열 반환, 
def create_chips(parent, num, color):
    chips = []
    for i in range(num):
        chips.append(Node(parent, glm.scale((0,0,0)), color, Obj(os.path.join(casino_path, "Chip.obj"))))
    
    return chips

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
    MVP_loc = glGetUniformLocation(shader_for_lighting, 'MVP')
    M_loc = glGetUniformLocation(shader_for_lighting, 'M')
    view_pos_loc = glGetUniformLocation(shader_for_lighting, 'view_pos')
    color_loc = glGetUniformLocation(shader_for_lighting, 'color') 
     
    # prepare vaos
    vao_cube = prepare_vao_cube()
    vao_frame = prepare_vao_frame()
    vao_grid_x = prepare_vao_grid_x()
    vao_grid_z = prepare_vao_grid_z()
    vao_drop_obj = prepare_vao_obj(Obj(""))

    # Casino nodes
    Table = Node(None, glm.scale((0,0,0)), glm.vec3(1,0,0), Casino_table_obj)
    Spade = Node(Table, glm.scale((0,0,0)), glm.vec3(0,1,0), Spade_card_obj)
    Dia = Node(Table, glm.scale((0,0,0)), glm.vec3(0,0,1), Diamond_card_obj)
    Heart = Node(Table, glm.scale((0,0,0)), glm.vec3(1,1,0), Heart_card_obj)
    Clover = Node(Table, glm.scale((0,0,0)), glm.vec3(0,1,1), Clover_card_obj)
    Chips1_of_S = create_chips(Spade, 2, glm.vec3(0,1,0))
    Chips2_of_S = create_chips(Spade, 2, glm.vec3(0,1,0))
    Chips1_of_D = create_chips(Dia, 2, glm.vec3(0,0,1))
    Chips2_of_D = create_chips(Dia, 2, glm.vec3(0,0,1))
    Chips1_of_H = create_chips(Heart, 2, glm.vec3(1,1,0))
    Chips2_of_H = create_chips(Heart, 2, glm.vec3(1,1,0))
    Chips1_of_C = create_chips(Clover, 2, glm.vec3(0,1,1))
    Chips2_of_C = create_chips(Clover, 2, glm.vec3(0,1,1))
    Card_nodes = [Spade, Dia, Heart, Clover]
    Chips_nodes = [Chips1_of_S, Chips2_of_S, Chips1_of_D, Chips2_of_D, Chips1_of_H, Chips2_of_H, Chips1_of_C, Chips2_of_C]

    # prepare casino nodes vaos
    vao_table = prepare_vao_obj(Table.obj)
    vaos_card = prepare_vaos_card(Card_nodes)
    vao_chip = prepare_vao_obj(Chip_obj)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #projection / orthogonal
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
        draw_frame(vao_frame, MVP, MVP_loc_frame)

        #바닥(xz)에 격자
        draw_grid(vao_grid_x,vao_grid_z, MVP, MVP_loc_frame)

        glUseProgram(shader_for_lighting)
        glUniform3f(view_pos_loc, eye_vec.x, eye_vec.y, eye_vec.z)
        glUniform3f(color_loc, 1, 0, 0)

        # obj파일이 처음 drop되었을 때
        if first_drop:
            click_H = 1
            drop_OBJ.set_path(drop_path)
            drop_OBJ.parser()

            drop_OBJ.display_objInfo()

            vao_drop_obj = prepare_vao_obj(drop_OBJ)

            first_drop = False
        
        # # animating
        # t = glfwGetTime()

        # # rotation
        # th = np.radians(t*90)
        # M = glm.translate(glm.vec3(0, 0 , np.sin(th/3) * 10))
        glUniformMatrix4fv(M_loc, 1, GL_FALSE, glm.value_ptr(M))
        if click_H == 1:
            num_of_vertices = drop_OBJ.get_num_of_vertices()
            # single_mesh_mode(vao_drop_obj, P*V*M, MVP_loc, num_of_vertices)
            draw_obj(vao_drop_obj, MVP, MVP_loc, num_of_vertices)
            
        elif click_H == -1:
            print("hierarchy")
            VP = P*V

            # draw Table
            draw_node_obj(vao_table, Table, VP, MVP_loc, color_loc)

            # draw Cards
            i = 0;
            for card in Card_nodes:
                draw_node_obj(vaos_card[i], card, VP, M_loc, color_loc)
                i +=1

            # draw Chips
            for chips in Chips_nodes:
                # transformate each chip
                for chip in chips:
                    draw_node_obj(vao_chip, chip, VP, MVP_loc, color_loc)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
