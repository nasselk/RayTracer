from glm import vec3
from classes.objects.sphere import Sphere
from classes.scene import Scene
from classes.material import Material
from classes.lights.light import Light
from scenes.box import createBox

def createMirrorSpheres(scene: Scene) -> None:
	createBox(scene)

	# Miroirs parfaits (argent)
	scene.addObjects(
		Sphere(center=vec3(-1.5, -1.5, -3), radius=1.2, material=Material(color=vec3(0.95, 0.95, 0.95), specular_color=vec3(0.95, 0.95, 0.95), diffuse=0.0, reflectivity=1.0, specular=1.0, shininess=512)),
		Sphere(center=vec3(1.5, -1.5, -3.5), radius=1.0, material=Material(color=vec3(0.95, 0.95, 0.95), specular_color=vec3(0.95, 0.95, 0.95), diffuse=0.0, reflectivity=1.0, specular=1.0, shininess=512)),
	)
	
	# Or métallique
	gold_color = vec3(1.0, 0.84, 0.0)
	
	scene.addObjects(
		Sphere(center=vec3(0, 1, -4), radius=0.5, material=Material(color=gold_color, specular_color=gold_color, diffuse=0.15, reflectivity=0.85, specular=1.0, shininess=256)),
	)
	
	scene.addLights(
		Light(origin=vec3(0, 2.5, -1), intensity=1.2),
	)