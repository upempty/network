
import unittest
import sys

print (sys.path)
#set PYTHONPATH=%PYTHONPATH%;C:\VSCode\board\structures
#above exception, then go windows setting by env to set via GUI
#python -m unittest tests\test_array.py -v

# ! important import package
from src.array import Array

#arr = Array(10)
class TestArray(unittest.TestCase):
    def setUp(self):
        self.arr = Array(10)
    def tearDown(self):
        self.arr.clear()

    def test_setitem(self):
        self.assertEqual(10, len(self.arr))
        self.arr[0] = 188
        self.assertEqual(188, self.arr[0])
    
    def test_clear(self):
        self.arr.clear(1)
        for i in range(len(self.arr)):
            self.assertEqual(1, self.arr[i])

    def test_iter(self):
        for i in range(10):
            self.arr[i] = i
        
        for j, e in enumerate(self.arr):
            self.assertEqual(j, e)
            
