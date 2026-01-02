# Class for the camera

from pyglm import glm
from classes.ray import Ray

class Camera():
    fov_y = 1

    screen_height = 0
    screen_width = 0

    position = [0,0,0]

    up_vector = [0,1,0]

    eye_to_world_matrix = glm.mat4x4()

    def __init__(self, fov_y, position, target, screen_width = 1920, screen_height = 1080) -> None:
        self.position = position
        self.fov_y = glm.radians(fov_y)
        self.screen_height = screen_height
        self.screen_width = screen_width
        view_matrix = glm.lookAt(position, target, self.up_vector)
        self.eye_to_world_matrix = glm.inverse(view_matrix)
    
    def ray(self, x, y):
        aspect_ratio = self.screen_width / self.screen_height
        
        origin = glm.vec3(self.position)

        direction = glm.vec3(
            ((x + 0.5) / self.screen_width * 2 - 1) * aspect_ratio * glm.tan(self.fov_y / 2),
            -((y + 0.5) / self.screen_height * 2 - 1) * glm.tan(self.fov_y / 2),
            -1
		)
        
        direction = glm.vec3(self.eye_to_world_matrix * glm.vec4(direction.x, direction.y, direction.z, 0.0))
        direction = glm.normalize(direction)
        
        return Ray(origin, direction)
    
    def resize(self, width: int, height: int) -> None:
        self.screen_width = width
        self.screen_height = height