from glm import vec3
from classes.objects.plane import Plane
from classes.scene import Scene
from classes.material import Material

def createBox(scene: Scene, left_color=vec3(1, 0, 0), right_color=vec3(0, 1, 0), back_color=vec3(1, 1, 1), top_color=vec3(1, 1, 1), bottom_color=vec3(1, 1, 1)) -> None:
	scene.addObjects(
		Plane(point=vec3(5, 0, 0), normal=vec3(-1, 0, 0), material=Material(color=right_color)), # Mur droit
		Plane(point=vec3(-5, 0, 0), normal=vec3(1, 0, 0), material=Material(color=left_color)), # Mur gauche
		Plane(point=vec3(0, 3, 0), normal=vec3(0, -1, 0), material=Material(color=top_color)), # Mur haut
		Plane(point=vec3(0, -3, 0), normal=vec3(0, 1, 0), material=Material(color=bottom_color)), # Mur bas
		Plane(point=vec3(0, 0, 5), normal=vec3(0, 0, -1), material=Material(color=back_color)), # Mur avant
		Plane(point=vec3(0, 0, -5), normal=vec3(0, 0, 1), material=Material(color=back_color)) # Mur arrière
	)