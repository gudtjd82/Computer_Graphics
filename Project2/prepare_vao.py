from OpenGL.GL import *
import glm
import numpy as np
from obj import *
from node import *

def prepare_vao_frame():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position               # color
         0.0,   0.0,    0.0,     1.0, 0.0, 0.0, # x-axis start
         100.0, 0.0,    0.0,     1.0, 0.0, 0.0, # x-axis end 
         0.0,   0.0,    0.0,     0.0, 1.0, 0.0, # y-axis start
         0.0,   100.0,  0.0,     0.0, 1.0, 0.0, # y-axis end 
         0.0,   0.0,    0.0,     0.0, 0.0, 1.0, # z-axis start
         0.0,   0.0,    100.0,   0.0, 0.0, 1.0, # z-axis end 
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_grid_x():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
        -100.0, 0.0, 0.0,  0.4, 0.4, 0.4, # x-axis start
         100.0, 0.0, 0.0,  0.4, 0.4, 0.4, # x-axis end 
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_grid_z():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         0.0, 0.0,-100.0,  0.4, 0.4, 0.4, # z-axis start
         0.0, 0.0, 100.0,  0.4, 0.4, 0.4, # z-axis end 
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_cube():
    vertices = glm.array(glm.float32,
        # position            color
        -1.0,  1.0,  1.0 ,  0, 0,.5, # v0
         1.0, -1.0,  1.0 ,  0, 0,.5, # v2
         1.0,  1.0,  1.0 ,  0, 0,.5, # v1
        -1.0,  1.0,  1.0 ,  0, 0,.5, # v0
        -1.0, -1.0,  1.0 ,  0, 0,.5, # v3
         1.0, -1.0,  1.0 ,  0, 0,.5, # v2
        -1.0,  1.0, -1.0 ,  0,.5, 0, # v4
         1.0,  1.0, -1.0 ,  0,.5, 0, # v5
         1.0, -1.0, -1.0 ,  0,.5, 0, # v6
        -1.0,  1.0, -1.0 ,  0,.5, 0, # v4
         1.0, -1.0, -1.0 ,  0,.5, 0, # v6
        -1.0, -1.0, -1.0 ,  0,.5, 0, # v7
        -1.0,  1.0,  1.0 ,  0,.5,.5, # v0
         1.0,  1.0,  1.0 ,  0,.5,.5, # v1
         1.0,  1.0, -1.0 ,  0,.5,.5, # v5
        -1.0,  1.0,  1.0 ,  0,.5,.5, # v0
         1.0,  1.0, -1.0 ,  0,.5,.5, # v5
        -1.0,  1.0, -1.0 ,  0,.5,.5, # v4
        -1.0, -1.0,  1.0 , .5, 0, 0, # v3
         1.0, -1.0, -1.0 , .5, 0, 0, # v6
         1.0, -1.0,  1.0 , .5, 0, 0, # v2
        -1.0, -1.0,  1.0 , .5, 0, 0, # v3
        -1.0, -1.0, -1.0 , .5, 0, 0, # v7
         1.0, -1.0, -1.0 , .5, 0, 0, # v6
         1.0,  1.0,  1.0 , .5, 0,.5, # v1
         1.0, -1.0,  1.0 , .5, 0,.5, # v2
         1.0, -1.0, -1.0 , .5, 0,.5, # v6
         1.0,  1.0,  1.0 , .5, 0,.5, # v1
         1.0, -1.0, -1.0 , .5, 0,.5, # v6
         1.0,  1.0, -1.0 , .5, 0,.5, # v5
        -1.0,  1.0,  1.0 , .5,.5, 0, # v0
        -1.0, -1.0, -1.0 , .5,.5, 0, # v7
        -1.0, -1.0,  1.0 , .5,.5, 0, # v3
        -1.0,  1.0,  1.0 , .5,.5, 0, # v0
        -1.0,  1.0, -1.0 , .5,.5, 0, # v4
        -1.0, -1.0, -1.0 , .5,.5, 0, # v7
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_obj(obj):
    # position vertices
    positions = obj.get_positions()

    # vertices_arr = []
    # # i = 0
    # # j = 0
    # for v in obj.get_positions():
    #     for p in v:
    #         vertices_arr.append(p)
    #         # if i % 3 == 2:
    #         #     for k in range(3):
    #         #         vertices_arr.append(normals[j + k])
    #         #     j += 3
    #         # i+=1
    # # print("vetices 1: \n", vertices)
    # np_arr = np.array(vertices_arr, np.float32)
    # vertices = glm.array(np_arr, data=glm.float32)

    # normals
    normals_arr = []
    normals = obj.get_normals()
    # for n in normals:
    #     for v in n:
    #         normals_arr.append(v)
    # np_arr = np.array(normals_arr, np.float32)
    # normals = glm.array(np_arr, data=glm.float32)
    
    # pIndices_arr = []
    # nIndices_arr = []
    indices_arr = []
    i = 0
    for f in obj.get_faces_4v():
        for i in range(1, len(f)-1):
            indices_arr.append(f[0])
            indices_arr.append(f[i])
            indices_arr.append(f[i+1])
            # nIndices_arr.append(f[0][1])
            # nIndices_arr.append(f[i][1])
            # nIndices_arr.append(f[i+1][1])
    for f in obj.get_faces_3v():
        for i in range(1, len(f)-1):
            indices_arr.append(f[0])
            indices_arr.append(f[i])
            indices_arr.append(f[i+1])
            # pIndices_arr.append(f[0][0])
            # pIndices_arr.append(f[i][0])
            # pIndices_arr.append(f[i+1][0])
            # nIndices_arr.append(f[0][1])
            # nIndices_arr.append(f[i][1])
            # nIndices_arr.append(f[i+1][1])
    for f in obj.get_faces_more():
        # print(f)
        for i in range(1, len(f)-1):
            indices_arr.append(f[0])
            indices_arr.append(f[i])
            indices_arr.append(f[i+1])
            # pIndices_arr.append(f[0][0])
            # pIndices_arr.append(f[i][0])
            # pIndices_arr.append(f[i+1][0])
            # nIndices_arr.append(f[0][1])
            # nIndices_arr.append(f[i][1])
            # nIndices_arr.append(f[i+1][1])
    # np_arr = np.array(pIndices_arr, np.uint32)
    # # print("Indice: \n", np_arr)
    # pIndices = glm.array(np_arr, dtype=glm.uint32)

    # np_arr = np.array(nIndices_arr, np.uint32)
    # nIndices = glm.array(np_arr, dtype=glm.uint32)

    # print("vertices: \n", vertices, "\n")
    # print("normals: \n", normals, "\n" )
    # print("pIndices: \n", pIndices, "\n")
    # print("nIndices: \n", nIndices, "\n" )
    # print("indices: \n", indices_arr)

    vertices = []
    for i in range(len(indices_arr)):
        p = indices_arr[i][0]
        if len(indices_arr[i]) < 2:
           vertex = positions[p] + [0,1,0]
        elif len(indices_arr[i]) >= 2:
            n = indices_arr[i][1]
            vertex = positions[p] + normals[n]
        vertices += vertex
    np_arr = np.array(vertices, np.float32)
    # print(np_arr)
    vertices = glm.array(np_arr, data=glm.float32)
    # np_arr = np.array(indices_arr, np.float32)
    # indices = glm.array(np_arr, data=glm.float32)
    
    VAO = glGenVertexArrays(1)  # create VAO 
    glBindVertexArray(VAO)      # activate VAO

    VBO = glGenBuffers(1)               # create two VBOs
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO[0] - positions

    # EBO = glGenBuffers(1)                       # create two EBOs
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)  # activate EBO 

    # copy vertex data to VBO[0]
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) 
    # # copy index data to EBO
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, pIndices.nbytes, pIndices.ptr, GL_STATIC_DRAW)

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vaos_card(nodes):
    vaos = []
    for n in nodes:
        vaos.append(prepare_vao_obj(n.obj))
    
    return vaos
