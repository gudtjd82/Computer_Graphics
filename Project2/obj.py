from node import *

class Obj:
    def __init__(self, path):
        # path
        self.path = path

        # OBJ File Name
        self.fileName = path.strip().split("/").pop()

        # arrays
        self.postions = []
        self.normals = []
        self.faces_3v = []
        self.faces_4v = []
        self.faces_more = []
    
    # obj file을 parsing -> vertex와 face를 배열에 저장
    def parser(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()

        # i = 0;
        for line in lines:
            tockens = line.strip().split()
            if len(tockens) > 0:
                if tockens[0] == "v":
                    vertex = [float(v) for v in tockens[1:]]
                    # print(i , "번째: ")
                    # print(vertex)
                    # print()
                    self.postions.append(vertex)
                
                elif tockens[0] == "vn":
                    vertex = [float(vn) for vn in tockens[1:]]
                    self.normals.append(vertex)
                
                elif tockens[0] == "f":
                    face = []
                    for x in tockens[1:]:
                        i_str = x.strip().split("/")

                        if len(i_str) > 2:
                            i_int = [int(i_str[0]) - 1, int(i_str[2]) - 1]
                            if i_int[0] < 0:
                                i_int[0] = len(self.postions) + i_int[0]
                            if i_int[1]< 0:
                                i_int[1] = len(self.normals) + i_int[1]
                        elif 0 < len(i_str) <= 2:
                            i_int = [int(i_str[0]) - 1]
                            if i_int[0] < 0:
                                i_int[0] = len(self.postions) + i_int[0]

                        

                        face.append(i_int)

                    if(len(face) == 3):
                        self.faces_3v.append(face)
                    elif(len(face) == 4):
                        self.faces_4v.append(face)
                    elif(len(face) > 4):
                        self.faces_more.append(face)
        # print("vertex position: \n", pVertices)
        # print("face_3v: \n", faces_3v)
        # print("\nface_4v: \n", faces_4v)
    
    # obj 정보 출력
    def display_objInfo(self):
        num_of_faces = len(self.faces_3v)+len(self.faces_4v)

        print()
        print("------------------------------------------------")
        print("OBJ File Name:", self.fileName)
        print("Total Number of Faces:", num_of_faces)
        print("Number of Faces with 3 Vertices:", len(self.faces_3v))
        print("Number of Faces with 4 Vertices:", len(self.faces_4v))
        print("Number of Faces with 5+ Vertices:", len(self.faces_more))
        print("------------------------------------------------")
        print()

    def set_path(self, path):
        self.path = path
        self.fileName = path.strip().split("/").pop()
    
    def get_fileName(self):
        return self.fileName
    def get_positions(self):
        return self.postions
    def get_normals(self):
        return self.normals
    def get_faces_3v(self):
        return self.faces_3v
    def get_faces_4v(self):
        return self.faces_4v
    def get_faces_more(self):
        return self.faces_more
    def get_num_of_vertices(self):
        num_of_triangles = 0
        for f in self.faces_more:
            tris = len(f) - 2
            num_of_triangles += tris
        return len(self.faces_3v)*3 + len(self.faces_4v)*2*3 + num_of_triangles * 3
