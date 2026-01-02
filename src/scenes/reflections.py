from glm import vec3
from classes.objects.sphere import Sphere
from classes.scene import Scene
from classes.material import Material
from classes.lights.light import Light
from scenes.box import createBox
import math

def createReflections(scene: Scene) -> None:
	#Sphère miroir entourée de sphères colorées
	createBox(scene)
	
	# Grande sphère miroir chrome au centre
	chrome_color = vec3(0.95, 0.95, 0.95)
	scene.addObjects(
		Sphere(center=vec3(0, -0.5, -3), radius=1.5, material=Material(color=chrome_color, specular_color=chrome_color, diffuse=0.0, reflectivity=1.0, specular=1.0, shininess=512)),
	)
	
	# Petites sphères colorées autour (plastique)
	colors = [
		vec3(0.9, 0.1, 0.1),    # Rouge
		vec3(0.1, 0.8, 0.1),    # Vert
		vec3(0.1, 0.2, 0.9),    # Bleu
		vec3(0.95, 0.9, 0.1),   # Jaune
		vec3(0.85, 0.1, 0.85),  # Magenta
		vec3(0.1, 0.85, 0.85),  # Cyan
	]
	
	for i, color in enumerate(colors):
		angle = i * math.pi / 3
		x = 2.5 * math.cos(angle)
		z = -3 + 2.5 * math.sin(angle)
		scene.addObjects(
			Sphere(center=vec3(x, -2, z), radius=0.4, material=Material(color=color, specular_color=vec3(1, 1, 1), diffuse=0.7, specular=0.6, shininess=64)),
		)
	
	scene.addLights(
		Light(origin=vec3(0, 2.5, -1), intensity=1.0),
		Light(origin=vec3(0, 0, 0), intensity=0.25),
	)

