from .mosaic import Mosaic
from .utils import (
  get_image_matrix, 
  open_image, 
  get_available, 
  get_color_score
  )

from .layer import Layer
from .piece import PieceList, Piece
from .layer import LayerList
from .fit import Fit, PieceFits
#Scorelist or LayerList

"""
color score (represents the difference in pixel values between the piece color and where it is being places 
size score (represents the area of the piece)

fits score (this can be useful for awkward sized large pieces, for example, a 10 x 2 piece based on size and color that was ranked soley on size and color would most likely not even be a candidate to be placed until the middle of the rendering process because it is not super large. However, by the middle of the rendering process the number of viable spots will have dramatically been reduced because of the pieces awkward size. For this reason, this score can be used so that pieces that have less viable options are placed to prevent them from never being palced in the the mosaic.)
"""
    
    
class MosaicMaker:
  def __init__(
    self, 
    input_file : str, 
    mosaic_size : tuple, 
    piecelist : PieceList, 
    layer_list : LayerList,
    ):

    '''
    input_file : str - PATH to the reference image. Brickify is built off of PIL so all formats PIL supports are supported by Brickify. 
    mosaic_size : tuple (width, height) -  of the mosaic. The image will be resized to these. Depending on the number of pieces, a very large mosaic_size might make the rendering process take very long. 
    piecelist : PieceList - should be a PieceList object. Which is basically a nice representation of a list of pieces. 
    layer_list : ScoreList - should be a list of ScoreLayers. ScoreLayers are how the image knows when to prioritize matchinng colors and when to prioritize using large lego pieces. 
    
    A class used to create objects that create mosaics. Could have been a function, but it's just a bit cleaner as a class. 
    '''
    
    self.size = mosaic_size

    img = open_image(input_file, mosaic_size)
    #dont touch this
    self._matrix = get_image_matrix(img)

    #can be tinkered with outside class
    self.piecelist = piecelist 
    self.layer_list = layer_list


  def _create_fits(self, piece : Piece, flipped : bool = False):
    '''
    piece : Piece
    flipped : orientation fo the piece. 
    
    creates all of the fits (places a piece can fit on the board and the pieces score at that location)
    returns a PieceFits objects which is a sorted version off the fits. 
    '''
    if flipped:
      size = (piece.size[1], piece.size[0])

    else:
      size = piece.size

    fits = []
    size_score = piece.area

    for location in get_available(self._matrix, size):
      layer = self.layer_list.get_layer(location, size)
      #don't really like this but am okay with it for now. 
      color_score = get_color_score(self._matrix, location, size, piece.color)
      
      total_score = (
        (color_score * layer.color_scale) 
        + 
        (size_score * layer.size_scale)
      )

      fits.append(Fit(piece, location, total_score, flipped))

    return PieceFits(self.size, fits)


  def _create_all_fits(self):
    '''
    runs the _create_fits method for all the pieces in self.piecelist
    '''
    all_piece_fits = {}

    for piece in self.piecelist:
      fits = [self._create_fits(piece)]
    
      if piece.width != piece.height:
        fits.append(self._create_fits(piece, True))

      all_piece_fits[piece] = fits 

    return all_piece_fits


  def create(self):
    
    '''
    Weights are used to influence scores. 
    For example, 
    '''
    self._all_piece_fits = self._create_all_fits()
    mosaic = Mosaic(self.size)
    #create mosaic before and add them in 
    while True:
      best = self._get_best_fit()
      
      if best is None:
        #no more pieces can be places
        break
      
      self.piecelist.use_piece(best.piece)
      
      mosaic.add_fit(best)
      self._adjust_fits(best)
    
    return mosaic


  def _adjust_fits(self, fit : Fit):
    """
    fit : Fit
    
    removes the fits that would interfere with a fit that has just been chosen (pieces that intersect)
    that way there are no overlapping pieces.
    """
    
    for pfits in list(self._all_piece_fits.values()):
      for pfit in pfits:
        pfit.adjust_fits(fit) 


  def _get_best_fit(self):
    """
    loops through all the PieceFits in _all_piece_fits and runs the get_best_fit() method for each PieceFit
    that returns the best fit for that specific piece. Then it ranks all the "best fits" and returns the best out of those
    """
    best = None
    remove = []

    for piece, pfits in self._all_piece_fits.items():
      for pfit in pfits:
        fit = pfit.get_best_fit()


        #remove the fits that have zero
        
        if fit is None or self.piecelist.get_quantity(fit.piece) == 0:
          remove.append(piece)
          break #prevents double removal breaks inner loop

        elif best is None or fit.score > best.score:
          best = fit

    for piece in remove:
      self._all_piece_fits.pop(piece)
    
    return best

