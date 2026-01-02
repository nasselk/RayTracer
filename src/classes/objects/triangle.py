from typing import Optional
from pyglm import glm
import sys
from classes.objects.object import Object
from classes.material import Material

class Triangle(Object):
    vertices: list[glm.vec3]

    def __init__(self, v0: glm.vec3, v1: glm.vec3, v2: glm.vec3, material: Optional[Material] = None) -> None:
        super().__init__(material)

        self.vertices = [v0,v1,v2]

    def hit(self, ray):
        edge1 = self.vertices[1] - self.vertices[0]
        edge2 = self.vertices[2] - self.vertices[0]

        pVec = glm.cross(glm.normalize(ray.direction), edge2)
        det = glm.dot(edge1, pVec)

        if abs(det) < sys.float_info.epsilon:
            return None
        
        invDet = 1.0 / det

        tVec = ray.origin - self.vertices[0]

        u = glm.dot(tVec, pVec) * invDet

        if u < 0.0 or u > 1.0:
            return None
        
        qVec = glm.cross(tVec, edge1)
        v = glm.dot(glm.normalize(ray.direction), qVec) * invDet
        if v < 0.0 or u+v > 1.0:
            return None
        
        p_t = glm.dot(edge2, qVec) * invDet

        if p_t > sys.float_info.epsilon:
            return p_t

    def getNormal(self, hitPoint: glm.vec3) -> glm.vec3:
        return glm.normalize(glm.cross(self.vertices[1]-self.vertices[0], self.vertices[2]-self.vertices[0]))