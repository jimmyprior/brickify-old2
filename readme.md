

# Brickify
 ![Hello Kitty](https://i.imgur.com/P48mSds.jpg)

## Example

```python
from brickify.brickify import MosaicMaker
from brickify.piece import Piece, PieceList
from brickify.layer import Layer, LayerList


#create a MosaicMaker object
maker = MosaicMaker(
	input_file="",
	mosaic_size=(96, 96),
	piece_list=piece_list,
	layer_list=layer_list,
) 

mosaic = maker.create()
mosaic.render().show()
```
## Explanation

Brickify uses four parameters to decide where to place pieces. The values of the parameters change depending on the location of the piece. Because of that, a score for each piece at each location is calculated and stored as a **"Fit"**. All of the fits for one piece are stored in classes called FitLists Storing the Fits this way allows them to be sorted easily and quickly indexed and manipulated. The score for each piece at a given location is calculated using this equation:
total_score = (size_score * size_scale) + (color_score * color_scale)

### Scores
#### size_score
**Info:** The size_score is the area of a piece. (constant no matter the location) 
**Why:** The size_score represents the idea that placing large pieces is better than placing a bunch of small ones. 
**Range:** 1 ≤ size_score ≤  ∞
 
 #### color_score
 **Info:**  The color_score represents the average difference per pixel between a piece and the reference image multiplied by negative one. It is multiplied by negative 1 because the greater the difference, the worse the piece and the reference image match. It changes depending on the location being compared and the color of the piece. 
**Why:** The color_score represents the idea that matching the piece color to the reference image is important. 
**Range:** -256 ≤ color_score ≤ 0

### Scales

Two weights can be applied to each score, a **color_scale** and a **size_scale**. 

These scales are not constant throughout the mosaic. The user manipulates **"layers"** to specify different locations with different scales. This is because different areas of an image might need more detail than others. 

*E.G. the background of an image might have a higher size_scale because it does not have to be as detailed. But a face in the center image might require a higher color_scale because it requires more detail.*


## Setup

  
  

## Objects

### Piece
**_brickify.piece.Piece_** - represents a brick

#### Parameters 
size : (tuple) e.g. (width, height)
color : (tuple) e.g. (red, green, blue)
code : (str) a unique identifier whether lego or made up to make reading the directions easier (optional)

#### Methods 

**_render(flipped : int)_** -> Image:
returns a render of a piece in the form of a PIL Image object. 

#### Example
```python
from birckify.piece import Piece
from PIL import Image
test = Piece(
	size =  (2,  4), 
	color =  (242,  112,  94), 
	code =  "optional code"
	)
test.render(True).save("test.jpg")
```
![test.jpg](https://i.imgur.com/sXcg7Le.jpg)

### PieceList
**_brickify.piece.PieceList_** what the mosaic uses to access the pieces. Allows the user to specify the quantity of the pieces they want to add to this list. 

#### Parameters 
None

#### Methods
**add_piece(piece : Piece, quantity : int)** -> None:
piece : Piece
quantity : int (the number of pieces to be added. if quantity = -1 *default*, it is considered unlimited)

#### Example
```python
from brickify.piece import Piece, PieceList

test = Piece((2,  4), (242,  112,  94))
piece_list = PieceList()
piece_list.add_piece(test, 10) #adds 10 2 x 4 pieces to the list
```

### Layer
**_brickify.layer.Layer_** specify an area of the mosaic and the scales in that area

#### Parameters
(color_scale :  int, size_scale :  int, included =  "all"):

#### Methods
These are class methods to make life easier. 
from_image(path :  str, size :  tuple, color_scale :  int, size_scale :  int):
from_coordinates(included, color_scale, size_scale):
from_box(left_corner, size, color_scale, size_scale):

#### Example 
```python
layer = Layer.from_box((10,10), (100,100), 5, 2)
#creates a box of width and height 100 where top_left is (10,10) and the bottom_right is (110, 110)
#all "Fits" in these sections will have their color_score multiplied by 5 and their size_score multiplied by 2
```

### LayerList

**_brickify.layer.LayerList_** - create a list of multiple layers. This is what should be provided to the MosaicMaker. 


### To Do
- Add a recolor function that will recolor an image before processing. Hopefully, this should make using layers less necessary and make the renders more detailed on more complex images
- Finish Mosaic class
	- Add direction class that generates detailed directions and building 	instructions
	- Add render method to PieceList class
- Organize code, consistent type hinting, spelling
- Better comments for each method / function / class that explain what it does
	- Finish docs and make them more detailed and comprehensible



