from OpenGL.GL import *
import glm

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