from classes.objects.object import Object
from classes.material import Material
from pyglm import glm
from classes.ray import Ray
from typing import Optional

class Sphere(Object):
	center: glm.vec3
	radius: float
	
	def __init__(self, center: glm.vec3, radius: float, material: Optional[Material] = None) -> None:
		super().__init__(material)

		self.center = center
		self.radius = radius

	def hit(self, ray: Ray) -> float | None:
		oc = ray.origin - self.center
		
		a = glm.dot(ray.direction, ray.direction)
		b = 2.0 * glm.dot(oc, ray.direction)
		c = glm.dot(oc, oc) - self.radius ** 2
		
		discriminant = b*b - 4*a*c
		
		if discriminant < 0:
			return None
		
		distance = glm.sqrt(discriminant)
		t1 = (-b - distance) / (2.0*a)
		t2 = (-b + distance) / (2.0*a)
		
		if t1 >= 0:
			return t1
		elif t2 >= 0:
			return t2
		else:
			return None

	def getNormal(self, hitPoint: glm.vec3) -> glm.vec3:
		return glm.normalize(hitPoint - self.center)