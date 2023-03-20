from OpenGL.GL import *
from glfw.GLFW import *
import glm

vertices = glm.array(glm.float32,
    -0.5, 0.5, 0.0, 
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0,
    0.5, 0.5, 0.0
    )

VAO = glGenVertexArrays(1)  
glBindVertexArray(VAO)  #activate VAO

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)

glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4*glm.sizeof(glm.float32), None)    #(index, size, type, normalized, stride, pointer)
glEnableVertexAttribArray(0)

glBindVertexArray(VAO)

glDrawArrays(GL_TRIANGLES, 0, 4)