from classes.objects.object import Object
from classes.lights.light import Light
from typing import List

class Scene:
	objects: List[Object]
	lights: List[Light]

	def __init__(self):
		self.objects = []
		self.lights = []

	def addObjects(self, *objects: Object) -> None:
		self.objects.extend(objects) # Ajoute plusieurs objets à la scène

	def addLights(self, *lights: Light) -> None:
		self.lights.extend(lights) # Ajoute plusieurs lumières à la scène

	def clear(self) -> None:
		self.objects = []
		self.lights = []