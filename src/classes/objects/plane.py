from typing import Optional
from classes.objects.object import Object
from classes.material import Material
from pyglm import glm

from classes.ray import Ray

class Plane(Object):
	point: glm.vec3
	normal: glm.vec3
	
	def __init__(self, point: glm.vec3, normal: glm.vec3, material: Optional[Material] = None) -> None:
		super().__init__(material)

		self.point = point
		self.normal = glm.normalize(normal)

	def hit(self, ray: Ray) -> float | None:
		D = -glm.dot(self.normal, self.point)

		numerator = -(D + glm.dot(self.normal, ray.origin))
		denominator = glm.dot(self.normal, ray.direction)
		
		if abs(denominator) < 1e-6:
			return None
		
		t = numerator / denominator
		
		if t >= 0:
			return t
		
		else:
			return None
	
	def getNormal(self, hitPoint: glm.vec3) -> glm.vec3:
		return self.normal