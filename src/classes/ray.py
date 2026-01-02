from pyglm import glm

class Ray:
	def __init__(self, origin: glm.vec3, direction: glm.vec3) -> None:
		self.origin = origin
		self.direction = glm.normalize(direction)