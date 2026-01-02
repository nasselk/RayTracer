from classes.renderer import Renderer
from classes.scene import Scene
from glm import vec3
from classes.camera import Camera
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SAMPLES, MAX_DEPTH

# Differente scenes
from scenes.main import createMain
from scenes.glass_bunny_spotlight import createGlassBunnySpotlight
from scenes.mirror_spheres import createMirrorSpheres
from scenes.glass_spheres import createGlassSpheres
from scenes.reflections import createReflections
from scenes.water_drop import createWaterDrop

def main():
	camera = Camera(fov_y=90, position=vec3(0, 0, 0), target=vec3(0, 0, -1))
	renderer = Renderer(camera, SCREEN_WIDTH, SCREEN_HEIGHT, SAMPLES, MAX_DEPTH)
	
	# Rendre toutes les scènes
	scenes = [
		("main", createMain),
	]
	
	for name, createScene in scenes:
		print(f"Rendering {name}...")

		scene = Scene()

		createScene(scene)

		renderer.clear()
		renderer.render(scene)
		renderer.save(f"./output/{name}.png")

		print(f"Saved {name}.png")
	
	print("All scenes rendered!")

if __name__ == "__main__":
	main()