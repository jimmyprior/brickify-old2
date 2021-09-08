from .sorts import ScoreSorted, LocationSorted
from .piece import Piece

#https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner

#presort the lists
#reduce time complexity by taking first one of each


#add these to the brickify 


class Fit:
  def __init__(
    self, 
    piece : Piece, 
    location : tuple, 
    score : int, 
    flipped : bool
    ):
    """
    piece : Piece,
    location : (x,y) 
    score : (color_score * color_scale) + (size_score * size_scale) 
    color_scale and size_scale depend of the profile. 
    sum of all the scoress
    flipped : orientation 

    new and improved. no longer contains mosaic. 
    Purley for storage. Better encapsilation 

    Represents a piece and a location on the image
    """
    #https://stackoverflow.com/a/48731059/13950701
    self.piece = piece
    self.location = location
    self.score = score
    self.flipped = flipped

  @property
  def size(self):
    if self.flipped:
      return (self.piece.size[1], self.piece.size[0])
    else:
      return self.piece.size
    
  def render(self):
    return self.piece.render(self.flipped)

  def __hash__(self):
    return hash((self.piece, self.location, self.flipped))

  def __eq__(self, other):
    return self.score == other.score

  def __lt__(self, other):
    return self.score > other.score




#I THINK THE FITS SHOULD BE PASSED TO THIS BUT IDK FOR SURE YET...

class PieceFits:

  
  #a nice interface for interacting with a piece and all of it's fits

  #this takes the piece and does the calcs to create fits and sort. Remove that step from all piece fits

  #i think the fits should be passed to this but idk for sure yet. 
  def __init__(self, mosaic_size : tuple, fits : list):
    #protects the two sorted lists nice interface api 
    '''
    what is this??? all the fits for a piece one piece, all the palces it can fit
    a fit repreesnets one place on teh mosaic a piece could potentially go. This class represetns all of the fits or in other words places a piece could be located on the mosaic. 

    I need this for the fast adjust 
    '''
    #eventually need to accunt for flipping orientation
    #proabably two (4) different lists and comapre the best 
    
    self.csort = ScoreSorted(fits)
    self.lsort = LocationSorted(mosaic_size, fits)


  def adjust_fits(self, fit):
    overlap = self.lsort.get_affected(fit)
    for fit_no_more in overlap:
      self.csort.remove_fit(fit_no_more)


  def get_best_fit(self):
    return self.csort.get_best_fit()



#easy sort with dunder methods atually idk cause it's in a  dict 




#technical improvements size matching (pieces with same size but different color no rerender)





#old stuff
  
