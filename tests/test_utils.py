import unittest

from brickify.utils import (
    open_image,
    compare_colors, 
    get_image_matrix,
    get_sub_matrix,
    get_sub_list,
    get_occupied,
    get_available,
    get_color_score,
)

BLACK = (0, 0, 0)
WHITE = (255,255,255)

class UtilsTest(unittest.TestCase):
    
    def setUp(self):
    
        self.matrix = [
            [WHITE, BLACK, WHITE, BLACK, BLACK, WHITE, WHITE, WHITE, BLACK, BLACK],
            [BLACK, BLACK, BLACK, WHITE, BLACK, WHITE, WHITE, BLACK, WHITE, WHITE],
            [BLACK, WHITE, BLACK, BLACK, WHITE, BLACK, WHITE, BLACK, WHITE, BLACK],
            [BLACK, BLACK, WHITE, BLACK, WHITE, WHITE, BLACK, WHITE, BLACK, WHITE],
            [WHITE, WHITE, BLACK, WHITE, BLACK, WHITE, BLACK, WHITE, WHITE, BLACK],
            [BLACK, BLACK, WHITE, WHITE, BLACK, BLACK, WHITE, BLACK, WHITE, WHITE],
            [BLACK, BLACK, WHITE, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK],
            [WHITE, WHITE, BLACK, WHITE, BLACK, BLACK, WHITE, BLACK, WHITE, WHITE],
            [BLACK, WHITE, BLACK, BLACK, BLACK, WHITE, BLACK, WHITE, BLACK, WHITE],
            [BLACK, BLACK, WHITE, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK],
        ]
        
        
        
    def test_compare_colors(self):
        
        self.assertEqual(
            compare_colors(WHITE, WHITE),
            0
        )
        
        self.assertEqual(
            compare_colors(BLACK, WHITE),
            255 * 3
        )
        
        self.assertEqual(
            compare_colors((0, 0, 255), WHITE),
            255 * 2
        )
        
            
    def test_get_image_matrix(self):
        #get_image_matrix()
        pass
        
    def test_get_sub_matrix(self):
        #get_sub_matrix()
        #not used
        pass
    
    def test_get_sub_list(self):
        location = (0,0)
        size = (2, 8)
        sublist = get_sub_list(self.matrix, location, size)
        
        
        for y in range(location[1], location[1] + size[1]):
            for x in range(location[0], location[0] + size[0]):
                index = (size[0] * y) + x
                self.assertEqual(self.matrix[y][x], sublist[index])
        

    
    def test_get_occupied(self):
        #get_occupied()
        #might get rid of  you
        pass
    
    def test_get_available(self):
        #get_available(matrix : list, size : tuple):
        self.assertEqual(
            len(get_available(self.matrix, (1,1))),
            len(self.matrix) * len(self.matrix[0])
        )
        
        self.assertEqual(
            len(get_available(self.matrix, (2,2))),
            (len(self.matrix) - 1) * (len(self.matrix[0]) - 1)
        )
    
        self.assertEqual(
            len(get_available(self.matrix, (5,2))),
            (len(self.matrix) - 1) * (len(self.matrix[0]) - 4)
        )    
        
        avail = get_available(self.matrix, (5,2))
        self.assertTrue((9,9) not in avail)
        self.assertTrue((6,0) not in avail)
        self.assertTrue((6,9) not in avail)

        self.assertTrue((5,8) in avail)
        self.assertTrue((0,0) in avail)
        self.assertTrue((2,3) in avail)

        
        
    def test_get_color_score(self):
        #get_color_score()
        pass
    
    