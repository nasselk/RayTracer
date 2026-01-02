from glm import vec3
from classes.objects.sphere import Sphere
from classes.scene import Scene
from classes.material import Material
from classes.lights.light import Light
from scenes.box import createBox

def createGlassSpheres(scene: Scene) -> None:
	#Trois sphères en verre avec différents IOR
	createBox(scene)
	
	scene.addObjects(
		# Verre
		Sphere(center=vec3(-2, -1.5, -3), radius=1.0, material=Material(color=vec3(1, 1, 1), diffuse=0.0, refractivity=1.0, IOR=1.5)),
		# Diamant
		Sphere(center=vec3(0, -1.5, -3.5), radius=1.0, material=Material(color=vec3(1, 1, 1), diffuse=0.0, refractivity=1.0, IOR=2.4)),
		# Eau
		Sphere(center=vec3(2, -1.5, -3), radius=1.0, material=Material(color=vec3(1, 1, 1), diffuse=0.0, refractivity=1.0, IOR=1.33)),
	)
	
	scene.addLights(
		Light(origin=vec3(0, 2.5, -1), intensity=1.2),
		Light(origin=vec3(-2, 1, 0), intensity=0.4),
	)