from pyglm import glm
from classes.model import Model

def parse_obj(file_name):
    current_text = None
    vertex_array = []
    faces_array = []

    with open(file=file_name) as f:
        for current_text in f:
            current_line = current_text.split(" ")
            if current_line[0] == "v":
                vertex = glm.vec3(float(current_line[1]), float(current_line[2]), float(current_line[3].rstrip()))
                vertex_array.append(vertex)
            elif(current_line[0] == "f"):
                face = [int(current_line[1])-1, int(current_line[2])-1, int(current_line[3].rstrip())-1]
                faces_array.append(face)

    return Model(vertex_array, faces_array)