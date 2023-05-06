from OpenGL.GL import *
import glm
from node import *

def draw_frame(vao, MVP, MVP_loc):
    glBindVertexArray(vao)
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glDrawArrays(GL_LINES, 0, 6)

def draw_cube(vao, MVP, MVP_loc):
    glBindVertexArray(vao)
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glDrawArrays(GL_TRIANGLES, 0, 36)
    

def draw_grid(vao_x, vao_z, MVP, MVP_loc):
    glBindVertexArray(vao_x)
    for i in range(-200, 200):
        MVP_grid_x = MVP * glm.translate(glm.vec3(0, 0, .5*i))
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP_grid_x))
        glDrawArrays(GL_LINES, 0, 6)

    glBindVertexArray(vao_z)
    for i in range(-200, 200):
        MVP_grid_z = MVP * glm.translate(glm.vec3(.5*i, 0, 0))
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP_grid_z))
        glDrawArrays(GL_LINES, 0, 6)

def draw_obj(vao, MVP, MVP_loc, num_of_vertices):
    glBindVertexArray(vao)
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    # print(vao)
    glDrawArrays(GL_TRIANGLES, 0, num_of_vertices)
    # glDrawElements(GL_TRIANGLES, num_of_vertices, GL_UNSIGNED_INT, None)
                  
def draw_node(vao, node, VP, MVP_loc, color_loc, obj):
    MVP = VP * node.get_global_transform() * node.get_shape_transform()
    color = node.get_color()


    glBindVertexArray(vao)
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glUniform3f(color_loc, color.r, color.g, color.b)
    # print(vao)

    num_of_vertices = obj.get_num_of_vertices()
    glDrawArrays(GL_TRIANGLES, 0, num_of_vertices)

def draw_node_arr(vao, nodes, VP, MVP_loc, color_loc, obj):
    for node in nodes:
        MVP = VP * node.get_global_transform() * node.get_shape_transform()
        color = node.get_color()


        glBindVertexArray(vao)
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        glUniform3f(color_loc, color.r, color.g, color.b)
        # print(vao)

        num_of_vertices = obj.get_num_of_vertices()
        glDrawArrays(GL_TRIANGLES, 0, num_of_vertices)
    # print("num of vertices: ", num_of_vertices)