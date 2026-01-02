from glm import vec3
from utils.parser import parse_obj
from classes.objects.octree import Octree
from classes.scene import Scene
from classes.material import Material
from classes.lights.light import Light
from scenes.box import createBox

def createMain(scene: Scene) -> None:
	# Create a box with custom wall colors
	createBox(
		scene,
	    left_color=vec3(1, 0, 0),    # Red
	    right_color=vec3(0, 0, 1),   # Blue
	    back_color=vec3(0, 1, 0),    # Green
	    top_color=vec3(0.5, 0, 0.5), # Purple
	    bottom_color=vec3(1, 1, 0)   # Yellow
	)

	# Add the bunny model
	bunny_model = parse_obj("src/assets/bunny.obj")
	bunny_model.scale(10)
	bunny_model.translate(vec3(0, -1, -2.5))
	bunny_model.generate_triangles()

	bunny = Octree(model=bunny_model, material=Material(color=vec3(1, 1, 1), diffuse=0.0, refractivity=1.0, IOR=1.5))
	bunny.generate_octree()
	scene.addObjects(bunny)

	# Add a single light source at the center top of the scene
	light_position = vec3(0, 2, -2.5)  # Center top
	light_color = vec3(1, 1, 1)        # White light
	scene.addLights(
	    Light(origin=light_position, intensity=1.5, color=light_color)
	)