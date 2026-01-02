from glm import vec3
from classes.objects.sphere import Sphere
from classes.objects.plane import Plane
from classes.scene import Scene
from classes.material import Material
from classes.lights.light import Light

def createWaterDrop(scene: Scene) -> None:
	#Goutte d'eau (sphère) sur un sol avec reflets
	
	# Sol avec reflet
	scene.addObjects(
		Plane(point=vec3(5, 0, 0), normal=vec3(-1, 0, 0), material=Material(color=vec3(0.9, 0.9, 0.9))),
		Plane(point=vec3(-5, 0, 0), normal=vec3(1, 0, 0), material=Material(color=vec3(0.9, 0.9, 0.9))),
		Plane(point=vec3(0, 3, 0), normal=vec3(0, -1, 0), material=Material(color=vec3(0.5, 0.7, 1.0))),  # Ciel bleu
		Plane(point=vec3(0, -2, 0), normal=vec3(0, 1, 0), material=Material(color=vec3(0.2, 0.2, 0.3), diffuse=0.3, reflectivity=0.7)),  # Sol réfléchissant
		Plane(point=vec3(0, 0, 5), normal=vec3(0, 0, -1), material=Material(color=vec3(0.9, 0.9, 0.9))),
		Plane(point=vec3(0, 0, -5), normal=vec3(0, 0, 1), material=Material(color=vec3(0.9, 0.9, 0.9))),
	)
	
	# Goutte d'eau (eau IOR = 1.33)
	scene.addObjects(
		Sphere(center=vec3(0, -0.5, -3), radius=1.5, material=Material(color=vec3(1, 1, 1), diffuse=0.0, refractivity=1.0, IOR=1.33)),
	)
	
	scene.addLights(
		Light(origin=vec3(2, 2.5, -1), intensity=1.2),
		Light(origin=vec3(-1, 1, 0), intensity=0.3),
	)