#! /usr/bin/env python3
#coding: utf-8

import sys
k = '中文support'
print ('{}: py version:{}\n'.format(k, sys.version[0:5]))

class Search:
    def __init__(self):
        pass

    def two_d_lookup(self,target, array):
        i = 0
        j = len(array[0]) - 1
        while (i < len(array) and j >= 0):
            base = array[i][j]
            if base == target:
                return True
            elif base < target:
                i = i + 1
            else:
                j = j - 1 
        return False

s = Search() 

print('====p1: two_d_lookup(self,target, array)')
arr = [[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]]
ret = s.two_d_lookup(4, arr)
print ('ret1 = {}: 4 in {}'.format(ret, arr))
ret = s.two_d_lookup(0, [[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]])
print ('ret2 = {}: 0 in {}'.format(ret, arr))
print('====p1: end\n')
