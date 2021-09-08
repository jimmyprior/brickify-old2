from PIL import Image
from .piece import Piece
#mosaic is what is returned by the renderer
from .fit import Fit
import random
import pickle


from .utils import get_occupied
from .piece import PieceList


SCALE = Piece.scale

class Mosaic:
  border = 1
  scale = 20
  
  def __init__(self, size : tuple):
    self.size = size
    self.fits = []
    #self.directions = Directions()

    #create the piecelist?

  def add_fit(self, fit : Fit):
    #print(len(self.fits))

    self.fits.append(fit)


  def render(self):

    scale = Piece.scale

    final = Image.new(
      'RGB', 
      (self.size[0] * scale, self.size[1] * scale)
    )


    for fit in self.fits:

      final.paste(
        im = fit.render(), 
        box=(
          fit.location[0] * scale, 
          fit.location[1] * scale
        )
      )

    return final

  @property
  def piecelist(self):
    pass
  
  
  @property
  def directions(self):
    #need to count the number of fits with each piece. 
    # or I could subtract from the original but it's probably not worth it. 
    #not implemented
    pass

  def save(self, name = None):
    if not name:
      name = f"mosaic{random.randint(1, 1000)}.pickle"
      
    with open(name, 'wb') as file:
      pickle.dump(self, file)
      
    



  



  