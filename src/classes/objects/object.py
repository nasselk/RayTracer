from abc import ABC, abstractmethod
from typing import Optional
from classes.ray import Ray
from pyglm import glm
from classes.material import Material

class Object(ABC):
	material: Material
    
	def __init__(self, material: Optional[Material] = None) -> None:
		if material is None:
			self.material = Material() # Matriaux par défaut
		else:
			self.material = material

	@abstractmethod
	def hit(self, ray: Ray) -> float | None:
		pass

	@abstractmethod
	def getNormal(self, hitPoint: glm.vec3) -> glm.vec3:
		pass