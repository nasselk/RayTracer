from classes.camera import Camera
from classes.scene import Scene
from random import random
from glm import vec3
import numpy as np
from PIL import Image
from pyglm import glm
from classes.ray import Ray
from typing import Optional
from constants import AMBIANT_LIGHT, EPSILON
from classes.objects.object import Object
from datetime import datetime

class Renderer:
	output: np.ndarray
	width: int
	height: int
	camera: Camera
	samples: int
	maxDepth: int
	
	def __init__(self, camera: Camera, width: int, height: int, samples: int = 1, maxDepth: int = 5) -> None:
		if samples < 1:
			raise ValueError("Samples must be at least 1")
		
		self.samples = samples # Nombre d'échantillons par pixel pour l'anti-aliasing
		self.camera = camera
		self.width = width
		self.height = height
		self.maxDepth = maxDepth # Profondeur maximale de récursion pour les rayons
		self.output = np.zeros((self.height, self.width, 3), dtype=np.float32)

		self.camera.resize(width, height) # Assure que la caméra est configurée pour la bonne taille d'image
		
	def render(self, scene: Scene, xOffset: int = 0, yOffset: int = 0, width: Optional[int] = None, height: Optional[int] = None) -> None:
		if width is None:
			width = self.width

		if height is None:
			height = self.height

		for y in range(yOffset, yOffset + height):
			for x in range(xOffset, xOffset + width):
				color = vec3(0, 0, 0) # Noir

				for _ in range(self.samples):
					color += self.computePixelColor(scene, x, y)

				self.output[y, x] = color.xyz / self.samples # Moyenne des échantillons

	def computePixelColor(self, scene: Scene, x: float, y: float) -> vec3:
		color = vec3(0, 0, 0) # Noir

		# Supersampling anti-aliasing
		if self.samples > 1:
			x += random() - 0.5
			y += random() - 0.5
			
		ray = self.camera.ray(x, y)
		color += self.traceRay(scene, ray)

		return color
	
	def traceRay(self, scene: Scene, ray: Ray, depth: int = 0) -> vec3:
		color = vec3(0, 0, 0) # Noir par défaut

		if depth < self.maxDepth:
			object, t = self.findClosestObject(scene, ray)

			if object:
				intersection = ray.origin + t * ray.direction
				normal = object.getNormal(intersection)
				viewDir = -ray.direction
				
				# Materiaux transparents (verre, eau)
				if object.material.refractivity > 0 and object.material.IOR > 1.0:
					# Calculer le coefficient de Fresnel
					fresnel = self.fresnel(ray.direction, normal, object.material.IOR)
					
					# Calculer les contributions de réflexion et de réfraction
					reflected_contribution = self.reflectRay(scene, ray, object, intersection, normal, depth)
					refracted_contribution = self.refractRay(scene, ray, object, intersection, normal, depth)
					
					# Donner la tinte de couleur du matériau réfractif
					refracted_contribution *= object.material.diffuse_color
					
					# Mélanger les contributions de réflexion et de réfraction avec Fresnel
					fresnel_color = reflected_contribution * fresnel + refracted_contribution * (1 - fresnel)

					color += fresnel_color * object.material.refractivity
				
				# Materiaux reflectifs (miroir et metaux)
				elif object.material.reflectivity > 0:
					reflected_color = self.reflectRay(scene, ray, object, intersection, normal, depth)
					
					# Teinter les réflexions par la couleur du métal (or, cuivre, etc.)
					reflected_color *= object.material.specular_color

					color += reflected_color * object.material.reflectivity
				
				# Materiaux diffus (plastique, bois)
				if object.material.diffuse > 0:
					# Prendre en compte la lumière ambiante
					diffuse_color = object.material.diffuse_color * AMBIANT_LIGHT

					# Ajouter la contribution de chaque source lumineuse
					for light in scene.lights:
						diffuse_color += light.getContribution(scene.objects, object, intersection, viewDir)

					color += diffuse_color * object.material.diffuse

		return color
	
	def findClosestObject(self, scene: Scene, ray: Ray) -> tuple[Optional[Object], float]:
		t = float("inf")
		object = None

		# Trouver l'objet le plus proche
		for obj in scene.objects:
			new_t = obj.hit(ray)

			if new_t and new_t < t:
				object = obj
				t = new_t

		return object, t

	def reflectRay(self, scene: Scene, ray: Ray, obj: Object, intersection: vec3, normal: vec3, depth: int) -> vec3:
		# S'assurer que la normale fait face au rayon incident
		if glm.dot(ray.direction, normal) > 0:
			normal = -normal
		
		# Calculer la direction réfléchie
		direction = glm.reflect(ray.direction, normal)
		
		# Décaler l'origine pour éviter l'auto-intersection
		reflection_origin = intersection + EPSILON * normal
		reflection = Ray(reflection_origin, vec3(direction))

		return self.traceRay(scene, reflection, depth + 1)
	
	def refractRay(self, scene: Scene, ray: Ray, obj: Object, intersection: vec3, normal: vec3, depth: int) -> vec3:
		# Determine if we're entering or exiting the object
		cos_theta = glm.dot(glm.normalize(ray.direction), normal)
		
		if cos_theta < 0:  # Entering the material
			# Ray going into object: air (n=1) to glass (n=IOR)
			# eta = n1/n2 = 1.0/IOR
			eta = 1.0 / obj.material.IOR
			outward_normal = normal
		else:  # Exiting the material
			# Ray leaving object: glass (n=IOR) to air (n=1)
			# eta = n1/n2 = IOR/1.0
			eta = obj.material.IOR
			outward_normal = -normal
		
		# Calculate refraction direction using Snell's law
		direction = vec3(glm.refract(glm.normalize(ray.direction), outward_normal, eta))
		
		# Check for total internal reflection (refract returns zero vector)
		if glm.length(direction) < EPSILON:
			# Total internal reflection - return reflection instead
			return self.reflectRay(scene, ray, obj, intersection, normal, depth)
		
		# Offset origin to avoid self-intersection (in opposite direction from reflection)
		refraction_origin = intersection - EPSILON * outward_normal
		refraction = Ray(refraction_origin, direction)
		
		return self.traceRay(scene, refraction, depth + 1)
	
	def fresnel(self, incident: vec3, normal: vec3, ior: float) -> float:
		# Calculer l'angle d'incidence
		cos_i = glm.dot(incident, normal)
		
		if cos_i < 0:
			cos_i = -cos_i
			r0 = ((1.0 - ior) / (1.0 + ior)) ** 2
			
		else:
			# Calculer l'angle de transmission en utilisant la loi de Snell
			sin_t2 = ior * ior * (1.0 - cos_i * cos_i)

			if sin_t2 > 1.0:
				return 1.0 # Réflexion totale interne
			
			cos_i = (1.0 - sin_t2) ** 0.5
			r0 = ((ior - 1.0) / (ior + 1.0)) ** 2
		
		return r0 + (1.0 - r0) * ((1.0 - cos_i) ** 5)

	def resize(self, width: int, height: int) -> None:
		self.width = width
		self.height = height

		self.camera.resize(width, height)

		self.output = np.zeros((self.height, self.width, 3), dtype=np.float32)

	def clear(self) -> None:
		self.output.fill(0)

	def save(self, path: Optional[str] = None) -> None:
		if path is None:
			now = datetime.now()
			date = now.strftime("%Y-%m-%d_%H-%M-%S")
			path = f"./output/render_{date}.png"

		rgb_image = (np.clip(self.output, 0.0,1.0) * 255.0).astype(np.uint8)
		image = Image.fromarray(rgb_image)
		image.save(path)