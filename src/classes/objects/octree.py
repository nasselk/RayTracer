from typing import Optional
from pyglm import glm
import sys

from classes.material import Material
from classes.objects.object import Object
from classes.objects.plane import Plane
from classes.model import Model

class Cell:
    def generate_planes(self):
        mid = (self.min + self.max) / 2.0
        self.planes.append(Plane( glm.vec3(self.min.x, mid.y, mid.z), glm.vec3(1.0,0.0,0.0)))
        self.planes.append(Plane(glm.vec3(self.max.x, mid.y, mid.z),glm.vec3(-1.0,0.0,0.0)))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, self.min.z),glm.vec3(0.0,1.0,0.0)))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, mid.z),glm.vec3(0.0,-1.0,0.0)))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, self.min.z),glm.vec3(0.0,0.0,1.0)))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, self.max.z),glm.vec3(0.0,0.0,-1.0)))
        
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.triangles = []
        self.planes = []
        self.children = []
        self.generate_planes()
    
    def hit(self, ray):
        """Check if ray hits cell's bounding box. Returns (tmin, tmax) or None."""
        tmin = 0.0
        tmax = float('inf')
        
        for i in range(3):
            origin = ray.origin[i]
            direction = ray.direction[i]
            box_min = self.min[i]
            box_max = self.max[i]
            
            if abs(direction) < 1e-8:
                # Ray parallel to slab - check if origin inside
                if origin < box_min or origin > box_max:
                    return None
            else:
                t1 = (box_min - origin) / direction
                t2 = (box_max - origin) / direction
                
                if t1 > t2:
                    t1, t2 = t2, t1
                
                tmin = max(tmin, t1)
                tmax = min(tmax, t2)
                
                if tmin > tmax:
                    return None
        
        return (tmin, tmax)

class Octree(Object):
    model = None
    min = glm.vec3(0.0,0.0,0.0)
    max = glm.vec3(0.0,0.0,0.0)
    num_cells = 0
    max_depth = 20
    root = None

    planes = []
    
    def compute_boundingBox(self):
        min = glm.vec3(sys.float_info.max, sys.float_info.max, sys.float_info.max)
        max = glm.vec3(-sys.float_info.max, -sys.float_info.max, -sys.float_info.max)
        for v in self.model.vertices:
            if v.x < min.x:
                min.x = v.x
            if v.y < min.y:
                min.y = v.y
            if v.z < min.z:
                min.z = v.z
            if v.x > max.x:
                max.x = v.x
            if v.y > max.y:
                max.y = v.y
            if v.z > max.z:
                max.z = v.z
        self.min = min
        self.max = max

    def __init__(self, model: Model, material: Optional[Material]=None):
        super().__init__(material)
        
        self.model = model
        self._last_hit_triangle = None  # Store last hit triangle for getNormal
        self.compute_boundingBox()
        self.root = Cell(self.min, self.max)
        self.num_cells = 1
        self.root.triangles = self.model.triangles
        for t in self.root.triangles:
            t.parent = self
    
    def isInCell(self, triangle, cell):
        eps = 1e-12
        for v in triangle.vertices:
            if (v.x >= cell.min.x - eps and v.x <= cell.max.x + eps and
                v.y >= cell.min.y - eps and v.y <= cell.max.y + eps and
                v.z >= cell.min.z - eps and v.z <= cell.max.z + eps):
                return True
        return False

    def subdivide_cell(self, cell, depth):
        if depth >= self.max_depth or len(cell.triangles) <= 100:
            return
        mid = (cell.min + cell.max) / 2
        cell.children = []
        cell.children.append(Cell(cell.min, mid))
        cell.children.append(Cell(glm.vec3(mid.x, cell.min.y, cell.min.z), glm.vec3(cell.max.x, mid.y, mid.z)))
        cell.children.append(Cell(glm.vec3(mid.x, cell.min.y, mid.z), glm.vec3(cell.max.x, mid.y, cell.max.z)))
        cell.children.append(Cell(glm.vec3(cell.min.x, cell.min.y, mid.z), glm.vec3(mid.x, mid.y, cell.max.z)))
        
        cell.children.append(Cell(glm.vec3(cell.min.x, mid.y, cell.min.z), glm.vec3(mid.x, cell.max.y, mid.z)))
        cell.children.append(Cell(glm.vec3(mid.x, mid.y, cell.min.z), glm.vec3(cell.max.x, cell.max.y, mid.z)))
        cell.children.append(Cell(glm.vec3(mid.x, mid.y, mid.z), glm.vec3(cell.max.x, cell.max.y, cell.max.z)))
        cell.children.append(Cell(glm.vec3(cell.min.x, mid.y, mid.z), glm.vec3(mid.x, cell.max.y, cell.max.z)))
        
        for triangle in list(cell.triangles):
            for c in cell.children:
                if self.isInCell(triangle, c):
                    c.triangles.append(triangle)
        cell.triangles = []
        for c in cell.children:
            self.subdivide_cell(c, depth +1)

    def generate_octree(self):
        self.subdivide_cell(self.root, 0)

    def hit(self, ray):
        """Returns closest t distance, or None if no hit."""
        t, triangle = self._hit_cell(self.root, ray)
        self._last_hit_triangle = triangle  # Store for getNormal/getColor
        return t
    
    def _hit_cell(self, cell, ray):
        """Recursively traverse octree to find closest triangle intersection."""
        # First check if ray hits this cell's bounding box
        box_hit = cell.hit(ray)
        if box_hit is None:
            return None, None
        
        closest_t = None
        closest_triangle = None
        
        # If this is a leaf node (has triangles, no children)
        if cell.triangles:
            for triangle in cell.triangles:
                t = triangle.hit(ray)
                if t is not None and t > 1e-6:
                    if closest_t is None or t < closest_t:
                        closest_t = t
                        closest_triangle = triangle
        
        # Recurse into children
        if cell.children:
            for child in cell.children:
                t, tri = self._hit_cell(child, ray)
                if t is not None:
                    if closest_t is None or t < closest_t:
                        closest_t = t
                        closest_triangle = tri
        
        return closest_t, closest_triangle

    def getNormal(self, hitPoint):
        """Return normal of the last hit triangle."""
        if self._last_hit_triangle:
            return self._last_hit_triangle.getNormal(hitPoint)
        
        return glm.vec3(0, 1, 0)  # Fallback
    
    def getColor(self, hitPoint, r=None, depth=None):
        """Return color from the octree's material."""
        return self.material.diffuse_color
