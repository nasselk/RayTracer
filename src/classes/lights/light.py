from classes.ray import Ray
from classes.objects.object import Object
from typing import List, Optional
from pyglm import glm
from constants import EPSILON

class Light:
	origin: glm.vec3
	intensity: float
	color: glm.vec3

	def __init__(self, origin: glm.vec3, intensity: float = 0.25, color: Optional[glm.vec3] = None) -> None:
		if intensity < 0:
			raise ValueError("Intensity must be non-negative")
		
		self.origin = origin
		self.intensity = intensity
		self.color = color or glm.vec3(1.0, 1.0, 1.0) # Lumière blanche par defaut

	def getContribution(self, objects: List[Object], object: Object, intersection: glm.vec3, viewDir: glm.vec3) -> glm.vec3:	
		# Si'l y a une occlusion, pas de contribution lumineuse
		if self.isInShadow(intersection, objects):
			return glm.vec3(0, 0, 0)
		
		# Calculer l'atténuation en fonction de la distance
		attenuation = self.getAttenuationFactor(intersection)

		Dl = glm.normalize(self.origin - intersection) # La direction de la lumière
		normal = object.getNormal(intersection) # La normale de la surface
		
		# Calculer les contributions diffuse et spéculaire
		diffuse_factor = self.diffuse(object, Dl, normal)
		specular_factor = self.specular(object, Dl, normal, viewDir)

		# Combine contributions
		diffuse_contribution = object.material.diffuse_color * diffuse_factor * self.color * attenuation
		specular_contribution = object.material.specular_color * specular_factor * self.color * attenuation
		
		return diffuse_contribution + specular_contribution
	
	def diffuse(self, object: Object, Dl: glm.vec3, normal: glm.vec3) -> float:						
		return object.material.diffuse * max(0, glm.dot(normal, Dl)) * self.intensity
	
	def specular(self, object: Object, Dl: glm.vec3, normal: glm.vec3, viewDir: glm.vec3) -> float:
		# Calculer la direction à mi-chemin entre la direction de la lumière et la direction de vue
		halfwayDir = glm.normalize(Dl + viewDir)
		
		# Calculer l'intensité spéculaire en utilisant le modèle de Phong
		specular_intensity = max(0, glm.dot(normal, halfwayDir)) ** object.material.shininess
		
		return object.material.specular * specular_intensity * self.intensity
	
	def getAttenuationFactor(self, intersection: glm.vec3) -> float:
		distance = glm.length(self.origin - intersection) # Distance entre la lumière et le point d'intersection

		return 1.0 / (1.0 + 0.09 * distance + 0.032 * distance ** 2) # Atténuation quadratique
	
	def isInShadow(self, intersection: glm.vec3, objects: List[Object]) -> bool:
		direction = self.origin - intersection
		distance = glm.length(direction)
		direction = glm.normalize(direction)
		
		# Créer un rayon d'ombre légèrement décalé pour éviter l'auto-occlusion
		shadowRayOrigin = intersection + EPSILON * direction
		
		ray = Ray(shadowRayOrigin, direction)
		
		for object in objects:
			t = object.hit(ray)

			if t is not None and t < distance:
				return True # L'objet bloque la lumière
			
		return False