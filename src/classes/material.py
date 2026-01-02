from typing import Optional
from pyglm import glm

class Material:
	diffuse_color: glm.vec3
	specular_color: glm.vec3
	diffuse: float # Reflexion diffuse entre 0 et 1 (Kd)
	specular: float # Reflexion speculaire entre 0 et 1 (Ks)
	shininess: float  # Brillance (n)
	reflectivity: float # Reflecitivité entre 0 et 1 (Kr)
	refractivity: float # Refractivité entre 0 et 1 (Kt)
	IOR: float # Indice de réfraction entre 1.0 et infini

	def __init__(self, color: Optional[glm.vec3] = None, specular_color: Optional[glm.vec3] = None, diffuse: float = 1.0, specular: float = 0.0, shininess: float = 32.0, reflectivity: float = 0.0, refractivity: float = 0.0, IOR: float = 1.0) -> None:
		total = diffuse + reflectivity + refractivity

		# Normaliser les composantes si la somme dépasse 1
		if total > 1:
			diffuse /= total
			reflectivity /= total
			refractivity /= total
			
		self.diffuse_color = color or glm.vec3(1, 1, 1) # Default to white
		self.specular_color = specular_color or glm.vec3(1, 1, 1) # Default to white
		self.specular = specular
		self.diffuse = diffuse
		self.reflectivity = reflectivity
		self.refractivity = refractivity
		self.shininess = shininess
		self.IOR = IOR

		self.validate() # Valider les valeurs du matériau


	def validate(self) -> None:
		if self.diffuse < 0 or self.diffuse > 1:
			raise ValueError("Diffuse component must be between 0 and 1")

		elif self.specular < 0 or self.specular > 1:
			raise ValueError("Specular component must be between 0 and 1")
		
		elif self.shininess < 1:
			raise ValueError("Shininess must be at least 1")
		
		elif self.reflectivity < 0 or self.reflectivity > 1:
			raise ValueError("Reflectivity must be between 0 and 1")
		
		elif self.refractivity < 0 or self.refractivity > 1:
			raise ValueError("Refractivity must be between 0 and 1")
		
		elif self.IOR < 1:
			raise ValueError("IOR must be at least 1")
		
		elif self.refractivity > 0 and self.IOR == 1.0:
			raise ValueError("Refractive materials must have IOR > 1.0 (e.g., glass = 1.5, water = 1.33)")
		
		elif self.IOR > 1.0 and self.refractivity == 0:
			raise ValueError("Materials with IOR > 1.0 must have refractivity > 0 to be transparent")
		
		elif self.refractivity > 0 and self.reflectivity > 0:
			raise ValueError("Materials cannot be both refractive and reflective - use refractivity for glass (Fresnel handles reflection)")

	def clone(self) -> "Material":
		return Material(self.diffuse_color, self.specular_color, self.specular, self.diffuse, self.shininess, self.reflectivity, self.refractivity, self.IOR)