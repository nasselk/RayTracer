from glm import vec3
from utils.parser import parse_obj
from classes.objects.octree import Octree
from classes.scene import Scene
from classes.material import Material
from classes.lights.spot_light import SpotLight
from scenes.box import createBox
import math

def createGlassBunnySpotlight(scene: Scene) -> None:
	createBox(scene)
	
	#Lapin en verre avec deux spotlights
	bunny_model = parse_obj("../assets/bunny.obj")
	bunny_model.scale(10)
	bunny_model.translate(vec3(0, -1, -2.5))
	bunny_model.generate_triangles()
	
	# Verre avec reflets
	bunny = Octree(model=bunny_model, material=Material(color=vec3(1, 1, 1), diffuse=0.0, refractivity=1.0, IOR=1.5))
	bunny.generate_octree()
	
	scene.addObjects(bunny)
	
	# Spotlights de chaque côté vers le bunny
	left_light_pos = vec3(-1.5, 1, -1)
	left_target = vec3(0, -0.5, -2.5)
	
	right_light_pos = vec3(1.5, 1, -1)
	right_target = vec3(0, -0.5, -2.5)
	
	warm_tint = vec3(1.0, 0.9, 0.85)
	
	scene.addLights(
		SpotLight(origin=left_light_pos, direction=left_target - left_light_pos, angle=math.radians(25), intensity=2.0, color=warm_tint, outer_angle=math.radians(35)),
		SpotLight(origin=right_light_pos, direction=right_target - right_light_pos, angle=math.radians(25), intensity=2.0, color=warm_tint, outer_angle=math.radians(35)),
	)