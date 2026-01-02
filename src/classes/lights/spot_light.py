from pyglm import glm
from glm import vec3
from classes.lights.light import Light
from classes.objects.object import Object
from typing import List, Optional
import math


class SpotLight(Light):
	direction: vec3
	angle: float
	outer_angle: float

	def __init__(self, origin: vec3, direction: vec3, angle: float, intensity: float, color: Optional[vec3] = None, outer_angle: Optional[float] = None):
		super().__init__(origin, intensity, color)

		self.direction = glm.normalize(direction)
		self.angle = angle  # L'angle du cône intérieur
		self.outer_angle = outer_angle if outer_angle else angle * 1.2 # L'angle du cône extérieur

	def getContribution(self, objects: List[Object], object: Object, intersection: vec3, viewDir: vec3) -> vec3:
		# Calculer la direction du spot vers le point d'intersection
		light_to_point = glm.normalize(intersection - self.origin)
		
		# Calculer l'angle entre la direction du spot et la direction vers le point
		cos_angle = glm.dot(light_to_point, self.direction)
		current_angle = math.acos(max(-1.0, min(1.0, cos_angle)))
		
		# Pas de lumière si en dehors du cone exterieur
		if current_angle > self.outer_angle:
			return glm.vec3(0, 0, 0)
		
		# Dégradé si c'est en dehors du cone interne
		if current_angle > self.angle:
			# Interpolation
			factor = 1.0 - (current_angle - self.angle) / (self.outer_angle - self.angle)
		else:
			# Luminosité complete
			factor = 1.0
		
		# Get base contribution from parent (handles shadows, diffuse, specular)
		contribution = super().getContribution(objects, object, intersection, viewDir)
		
		# Apply cone falloff
		return contribution * factor