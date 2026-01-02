from classes.objects.triangle import Triangle
from pyglm import glm

class Model():
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.triangles = []

    def generate_triangles(self):
        list_of_triangles = []
        for f in self.faces:
            v0 = self.vertices[f[0]]
            v1 = self.vertices[f[1]]
            v2 = self.vertices[f[2]]
            triangle = Triangle(v0, v1, v2)
            list_of_triangles.append(triangle)
        self.triangles =  list_of_triangles

    def barycentre(self):
        barycentre = glm.vec3(0.0)
        for v in self.vertices:
            barycentre += v
        barycentre /= len(self.vertices)
        return barycentre
    
    def translate(self, translation_vector: glm.vec3) -> None:
        for i in range(len(self.vertices)):
            self.vertices[i] += translation_vector
    
    def scale(self, scale_factor: float) -> None:
        for i in range(len(self.vertices)):
            self.vertices[i] *= scale_factor
    
    def scale_uniform(self, scale_factor, center=None):
        """
        Scale uniformément le modèle.
        - scale_factor: scalaire ou glm.vec3 (si scalaire, uniforme).
        - center: glm.vec3 optionnel, point autour duquel scaler. Par défaut le barycentre.
        """
        # normaliser scale_factor en vec3
        if isinstance(scale_factor, (int, float)):
            s = glm.vec3(float(scale_factor), float(scale_factor), float(scale_factor))
        else:
            s = glm.vec3(scale_factor)

        if center is None:
            center = self.barycentre()
        else:
            center = glm.vec3(center)

        for i in range(len(self.vertices)):
            v = glm.vec3(self.vertices[i])
            # translation au centre, scale, puis retour
            self.vertices[i] = center + (v - center) * s


    def rotate(self, x: float, y: float, z: float, center=None):
        """
        Rotate le modèle autour des axes X, Y et Z.
        - x, y, z: angles en degrés.
        - center: glm.vec3 optionnel, point autour duquel tourner. Par défaut le barycentre.
        """
        if center is None:
            center = self.barycentre()
        else:
            center = glm.vec3(center)

        # Convertir les angles en radians
        ax = glm.radians(x)
        ay = glm.radians(y)
        az = glm.radians(z)

        # Matrices de rotation
        Rx = glm.mat3(
            1, 0, 0,
            0, glm.cos(ax), -glm.sin(ax),
            0, glm.sin(ax), glm.cos(ax)
        )

        Ry = glm.mat3(
            glm.cos(ay), 0, glm.sin(ay),
            0, 1, 0,
            -glm.sin(ay), 0, glm.cos(ay)
        )

        Rz = glm.mat3(
            glm.cos(az), -glm.sin(az), 0,
            glm.sin(az), glm.cos(az), 0,
            0, 0, 1
        )

        R = Rz * Ry * Rx  # Ordre des rotations ZYX

        for i in range(len(self.vertices)):
            v = glm.vec3(self.vertices[i])
            # translation au centre, rotation, puis retour
            self.vertices[i] = center + R * (v - center)