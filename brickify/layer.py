from .utils import open_image, get_image_matrix, get_occupied

class Layer:
  def __init__(
    self, 
    color_scale : int, 
    size_scale : int, 
    included = "all"
    ): 
    self.color_scale = color_scale
    self.size_scale = size_scale
    self.included = included


  @classmethod
  def from_image(
    cls, 
    path : str, 
    size : tuple, 
    color_scale : int, 
    size_scale : int
    ):
    """
    Eliminates everything that is not white. 
    """
    #self.coordinates = []
    included = set()
    img = open_image(path, size)
    data = get_image_matrix(img)
    for x in range(len(data[0])):
      for y in range(len(data)):
        if data[y][x] != (255,255,255):
          included.add((x,y))
    
    return cls(color_scale, size_scale, included)


  @classmethod
  def from_coordinates(cls, included, color_scale, size_scale):
    return cls(color_scale, size_scale, included)


  @classmethod
  def from_box(cls, left_corner, size, color_scale, size_scale):
    included = set()
    for y in range(left_corner[1], left_corner[1] + size[1]):
      for x in range(left_corner[0], left_corner[0] + size[0]):
        included.add((x, y))
  
    return cls(color_scale, size_scale, included)
  
  
  def check_coords(self, coords):
    for location in coords:
      if location not in self.included:
        return False
    
    return True
        
        
    
  
  
  

  
class LayerList:
  def __init__(self, default_color_scale = 1, default_size_scale = 1):
    self.layers = []
    self.add_layer(
      Layer(default_color_scale, default_size_scale)
    )
      
  def add_layer(self, layer):
    #add layer should have the scales not Layer
    self.layers.insert(0, layer)


  def get_layer(self, top_left, size):
    
    for layer in self.layers:
      if layer.included == "all":
        return layer
      
      #better way to check?
      coords = get_occupied(top_left, size)  
      if layer.check_coords(coords):
        return layer
      
    
