from OpenGL.GL import *
import glm
import numpy as np

def prepare_vao_frame():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         0.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis start
         100.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis end 
         0.0, 0.0, 0.0,  0.0, 1.0, 0.0, # y-axis start
         0.0, 100.0, 0.0,  0.0, 1.0, 0.0, # y-axis end 
         0.0, 0.0, 0.0,  0.0, 0.0, 1.0, # z-axis start
         0.0, 0.0, 100.0,  0.0, 0.0, 1.0, # z-axis end 
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

def prepare_vao_obj(pVertices, nVertices, faces_3v, faces_4v, faces_more):
    vertices_arr = []
    i = 0
    for v in pVertices:
        for p in v:
            vertices_arr.append(p)
            if i % 3 == 2:
                if i % 2 == 0:
                    vertices_arr.append(1.0)
                    vertices_arr.append(0)
                    vertices_arr.append(1.0)
                else:
                    vertices_arr.append(0)
                    vertices_arr.append(1.0)
                    vertices_arr.append(1.0)
                    # 2 5 8 11 14 17
            i+=1
    # print("vetices 1: \n", vertices)
    np_arr = np.array(vertices_arr, np.float32)
    vertices = glm.array(np_arr, data=glm.float32)
    
    
    indices_arr = []
    i = 0;
    for f in faces_4v:
        # print(i, "번째 f: ", f)
        v1 = f[0][0]
        v2 = f[1][0]
        v3 = f[2][0]
        v4 = f[3][0]
        indices_arr.append(v1)
        indices_arr.append(v2)
        indices_arr.append(v3)
        indices_arr.append(v1)
        indices_arr.append(v3)
        indices_arr.append(v4)
    for f in faces_3v:
        v1 = f[0][0]
        v2 = f[1][0]
        v3 = f[2][0]
        indices_arr.append(v1)
        indices_arr.append(v2)
        indices_arr.append(v3)
    np_arr = np.array(indices_arr, np.uint32)
    # print("Indice: \n", np_arr)
    indices = glm.array(np_arr, dtype=glm.uint32)
    

    # vertices = glm.array(glm.float32,
    #  1.,       -1.,       -1.,        1.,        1.,        1.,        
    #  1.,       -1.,        1.,        1.,        1.,        1.,       
    # -1.,       -1.,        1.,        1.,        1.,        1.,       
    # -1.,       -1.,       -1.,        1.,        1.,        1.,        
    #  1.,        1.,      -0.999999,   1.,        1.,        1.,        
    # 0.999999,   1.,        1.000001,  1.,        1.,        1.,       
    # -1.,        1.,        1.,        1.,        1.,        1.,
    # -1.,        1.,       -1.,        1.,        1.,        1.,      
    # )

    # indices = glm.array(glm.uint32, 
    # 1, 3, 0, 
    # 7, 5, 4, 
    # 4, 1, 0, 
    # 5, 2, 1, 
    # 2, 7, 3, 
    # 0, 7, 4, 
    # 1, 2, 3, 
    # 7, 6, 5, 
    # 4, 5, 1, 
    # 5, 6, 2, 
    # 2, 6, 7, 
    # 0, 3, 7,
    # )

    # print("vertices2: \n", vertices2, "\n")
    # print("vertices: \n", vertices, "\n")
    # print("indices2: \n", indices2, "\n")
    # print("indices: \n", indices, "\n")
    # print("vertices2 == vertices: ", (vertices2 == vertices))
    # print("indices2 == indices: ", (indices2 == indices))
    
    VAO = glGenVertexArrays(1)  # create VAO 
    glBindVertexArray(VAO)      # activate VAO

    VBO = glGenBuffers(1)               # create VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO 

    EBO = glGenBuffers(1)                       # create EBO
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)  # activate EBO 

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) 

    # copy index data to EBO
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy index data to the currently bound element buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO