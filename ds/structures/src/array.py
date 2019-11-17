import ctypes
class Array:
    def __init__(self, size):
        self._size = size;
        pyArrType = ctypes.py_object * size
        self._elems = pyArrType()
        #print ('invoked Array')
        self.clear(None)
    
    def __len__(self):
        return self._size
    
    def __getitem__(self, index):
        return self._elems[index]
    
    def __setitem__(self, index, value):
        self._elems[index] = value
    
    def clear(self, value = None):
        for i in range(len(self)):
            self._elems[i] = value
    
    def __iter__(self):
        return _ArrayIterator(self._elems)

class _ArrayIterator:
    def __init__(self, items):
        self._arr_ref = items
        self._cur_index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur_index < len(self._arr_ref):
            entry = self._arr_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration

