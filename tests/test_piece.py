from unittest import TestCase
from brickify.piece import Piece, PieceList

#https://code.tutsplus.com/tutorials/write-professional-unit-tests-in-python--cms-25835


 

class PieceTest(TestCase):
 
    def setUp(self):
        self.width = 8
        self.height = 16
        self.color = (255,255,255)
        self.quantity = 10
        
        self.piece = Piece(
            size = (self.width, self.height), 
            color = self.color, 
            quantity = self.quantity
        )
        
 
    def test_piece_size(self):
        self.assertEqual(self.piece.width, self.width)
        self.assertEqual(self.piece.height, self.height)
        
    
    def test_piece_render(self):
        render = self.piece.render(False)
        size = (self.width * Piece.scale, self.height * Piece.scale)
        self.assertEqual(render.size, size)
    
    
    def test_piece_equal_size_flip(self):
        #check and make sure two pieces where the width and height are swapped are still equal
        test_piece = Piece(
            size = (self.height, self.width), 
            color = self.color, 
            quantity = 5,
        )
        
        self.assertEqual(self.piece, test_piece)
        
        
    def test_piece_not_equal_size(self):
        test_piece = Piece(
            size = (2, 2), 
            color = self.color, 
            quantity = self.quantity,
        )
        
        self.assertNotEqual(self.piece, test_piece)
    
    
    def test_piece_not_equal_color(self):
        test_piece = Piece(
            size = (self.width, self.height), 
            color = (100, 100, 100), 
            quantity = self.quantity
        )
        
        self.assertNotEqual(self.piece, test_piece)        
        

    
class PieceListTest(TestCase):
    def setUp(self):
        self.piece = Piece(
            size = (8,16), 
            color = (255, 255, 255), 
            quantity = 10
        )
        
        self.piecelist = PieceList([self.piece])
        
    
    def test_add_same_piece(self):
        original_length = self.piecelist.quantity
        original_quantity = self.piece.quantity        
        
        self.piecelist.add_piece(self.piece)
        
        self.assertEqual(original_length, self.piecelist.quantity)
        self.assertEqual(original_quantity * 2, self.piece.quantity)
        

    def test_add_different_piece(self):
        original_length = self.piecelist.quantity
        
        self.piecelist.add_piece(
            Piece(
                size = (2, 6), 
                color = (100, 100, 100), 
                quantity = 5
            )
        )
        
        self.assertNotEqual(original_length, self.piecelist.quantity)
        
            
