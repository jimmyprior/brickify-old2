from PIL import Image, ImageDraw, ImageOps
import json

class Piece:
  '''
  border : int the thickness of the piece border. Defaults to one. 
  scale : int | how many pixels are in a stud. e.g. (1,1) studs -> (20, 20) pixels  (img size)
  '''
  border = 1
  scale = 20

  def __init__(
    self, 
    size: tuple, 
    color: tuple, 
    code: str = None
    ):
    '''
    size : (tuple) e.g. (width, height)
    color : (tuple) e.g. (red, green, blue)
    code : (str) a unique identifier whether lego or made up to make reading the directions easier
    '''
    self.code = code
    self.width = size[0]
    self.height = size[1]
    self.size = size
    self.area = self.width * self.height
    self.color = color

    #scaled getters and not scaled getters
  
  def render(self, flipped : bool) -> Image:
    #needs to take flipped or should be moooved up the piecelist level. probablt that!!!
    '''
    just in case anything gets changed, the image is rerendered when this is accessed. 
    returns a rendering of the piece
    '''
    if flipped:
      width = self.height
      height = self.width

    else:
      width = self.width
      height = self.height

    brick_size = (width * self.scale, height * self.scale)
    image = Image.new("RGB", brick_size)
    one_by_one = self._render_1x1()

    for x in range(width):
      for y in range(height):
        image.paste(im=one_by_one, box=(x*self.scale, y*self.scale))

    resized = image.resize((width * self.scale - 2 * self.border, height * self.scale - 2 * self.border))
    bordered = ImageOps.expand(resized, border=self.border, fill='black')
    return bordered


  def _render_1x1(self) -> Image:
    '''
    Renders a 1x1 lego piece that is used to make up the brick
    For internal use only, this will not have a border so to get actual 1x1 brick use render method. 
    The cirlce is 80% of the original. If for some reason this needs changing, modify the .1 and .9 values. They represent box of ellipse. (0,0) being top left
    '''
    square = (self.scale, self.scale)
    circle = (self.scale*.1,self.scale *.1, self.scale*.9,self.scale*.9)

    image = Image.new("RGB", square, self.color)
    
    draw = ImageDraw.Draw(image)
    draw.ellipse(circle, outline='black', width=self.border)
    
    return image

  
  def __str__(self):
    '''
    printable version of the piece. really has no use other than debugging and using a duder method. 
    '''
    return(
      f"""Code: {str(self.code)}"""
    )

  def __eq__(self, piece):
    '''
    so that unlimited piecelist can make sure two of the same piece are not in the same list. That just does not make sense.
    additionally for the count method 
    '''
    return (
      (
        (piece.width == self.width and piece.height == self.height)
        or 
        (piece.width == self.height and piece.height == self.width)
      )
      and 
      (
        piece.color == self.color
      )
    )


  def __hash__(self):
    return hash((self.size, self.color))

  @property
  def json(self):
    return {
      "size" : self.size,
      "color" : self.color,
      "code" : self.code
    }



class PieceList:

  def __init__(self):
    """
    Stores the pieces and the amount of each piece
    """
    self.pieces = {}

  
  def add_piece(self, piece : Piece, quantity : int = -1):
    """
    piece : Piece
    quantity : int (the number of pieces to be added. if quantity = False, it is considered unlimited)
    add pieces to the piecelist
    """
    check = self.pieces.get(piece)
    
    if check and check > 0:
      #this should not be true if quantity = False so we should be good
      self.pieces[piece] += quantity
    
    else:
      #means that it does not exist and we have to create it
      self.pieces[piece] = quantity
      #otherwise it equals false and there are an unlimted number 


  def __iter__(self):
    for piece in list(self.pieces.keys()):
      yield piece
      
      
  def get_quantity(self, piece : Piece):
    return self.pieces[piece]


  def use_piece(self, piece : Piece):
    self.pieces[piece] -= 1


  def render(self):
    """
    Visual Representation of the pieces
    """
    pass

  def get_list(self):
    #rename
    pieces = []
    for piece, quantity in self.pieces.items():
      json = piece.json
      json["quantity"] = quantity
      pieces.append(json)
    return pieces



