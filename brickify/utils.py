#Handles a lot of the image and matrix operations. 
#A lot of the ugly functions that do the heavy lifting that I did not want cluttering the classes. 

from PIL import Image


class Matrix:
  "easy way to deal with the pixels???"
  pass


def open_image(path : str, size : tuple = None):
  """
  path : (str) complete path to an image | e.g. C:\Users\USER\Desktop\image.jpg
  size : (tuple) size the image should be resized to after it's opened 
  
  Opens an image using PIL and resizes it. 
  
  -> (Image)   
  """
  
  image = Image.open(path)
  if size:
    return image.resize(size)
  
  return image



def compare_colors(rgb1 : tuple, rgb2 : tuple):
  """
  rgb1 : (tuple) should be in (red, green, blue) or (red, green, blue, trans) depending on format
  rgb2 : (tuple) should be in (red, green, blue) or (red, green, blue, trans) depending on format
  
  Compares two pixels and returns the difference between them
  
  -> (int) difference between the two pixels
  """
  
  return (
    abs(rgb1[0] - rgb2[0]) +
    abs(rgb1[1] - rgb2[1]) + 
    abs(rgb1[2] - rgb2[2])
  )


def get_image_matrix(image : Image):
  """
  image : (Image) should be the Image object from PIL. 
  
  takes an image and returns a list of all the pixel values.
  
  -> (list) difference between the two pixels
  e.g. 
  [
    [(255,255,255), (255,255,255)], 
    [(255,255,255), (255,255,255)],
  ]
  """
  
  size = image.size
  blob = list(image.getdata())
  matrix = []
  last = 0
  for _ in range(size[1]):
    matrix.append(blob[last : last + size[0]])
    last += size[0]

  return matrix 


def get_sub_matrix(matrix : list, top_left : tuple, size : tuple):
  """
  matrix : (list) a nested list 
  top_left : (tuple) e.g. (x, y) top_left coordinate of a block 
  size : the size of the sub piece
  """
  sub_matrix = []
  for row_index in range(top_left[1], top_left[1] + size[1]):
    row = matrix[row_index][top_left[0] : top_left[0] + size[0]]
    sub_matrix.append(row)
    #make sure this is inclusive

  return sub_matrix


def get_sub_list(matrix : list, top_left : tuple, box_size : tuple):
  """
  matrix : (list) a nested list 
  top_left : (tuple) e.g. (x, y) top_left coordinate of a box 
  box_size : (tuple) size of the piece (width, height)

  """
  
  #not sure if I will keep this or just merge it all into a custom object...
  sub_list = []
  for row_index in range(top_left[1], top_left[1] + box_size[1]):
    for rgb in matrix[row_index][top_left[0] : top_left[0] + box_size[0]]:

      sub_list.append(rgb)
    #make sure this is inclusive

  return sub_list



def get_occupied(top_left : tuple, size : tuple):
  """
  top_left : (tuple) e.g. (x, y) top_left coordinate of a box 
  size : (tuple) e.g. (width, height) size of a piece
  
  returns a list of coordinates (x,y) that a piece would occupy
  
  -> (list) e.g. for a piece of size (4, 1) at (0, 20) 
  returns [(0, 20), (1, 20), (2, 20), (3, 20)]
  """
  occupied = []
  for col in range(top_left[0], top_left[0] + size[0]):
    for row in range(top_left[1], top_left[1] + size[1]):
      occupied.append((col, row))
  return occupied


def get_available(matrix_size : list, box_size : tuple):
  """
  matrix_size : (tuple) size of the mosaic (width, height)
  box_size : (tuple) size of the piece (width, height)
  
  -> (list) Returns a list of tuples (x,y) that represent the top_left coordinates
  of all the spots where a piece of (width, height) could fit 
  """

  available = []

  #check if inclusive
  for x in range(matrix_size[0] + 1 - box_size[0]):
    for y in range(matrix_size[1] + 1 - box_size[1]):
      available.append((x,y))

  return available



def get_color_score(matrix, location, size, pcolor):
  #this really does not belong here
  #should be moved to fit and fits will do the scoring. 
  #layers should be added to the fits
  
  #the flip is taken care of upstream no worries!
  length, width = size #might need to flip -> na do that upstream 
  mini = get_sub_list(matrix, location, (length, width))
  difference = 0
  for pixel in mini:
    difference += compare_colors(pixel, pcolor)
  return difference / -(size[0] * size[1])


