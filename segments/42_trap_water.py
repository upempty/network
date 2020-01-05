class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int

        | 
        | | .

        |   |
        | | |

        |
        | | |


        | |

        . |

        """
        count = len(height)
        if count <= 2:
            return 0

        #principle!
        #fill_on_curr -- return 0 or num units.
        #move_to_next
        #Note: first and last shall be not possible to be filled
        prev_max = 0; next_max = 0
        total = 0; units = 0
        recheck = True; next_max_ind = 0
        for ind in range(1, count-1):
            #units = fill_on_curr
            curr = height[ind]
            #prev_max
            if prev_max < height[ind-1]:
                prev_max = height[ind-1]
            #next_max
            if ind == next_max_ind and height[ind] == next_max:
                recheck = True
                next_max = 0
                next_max_ind = 0
            if recheck == True:
                for j in range(ind+1, count):
                    if next_max <= height[j]:
                        next_max = height[j]
                        next_max_ind = j
                recheck = False


            #check fill current or not
            if prev_max <= curr:
                units = 0
            elif prev_max > curr and curr >= next_max:
                units = 0
            elif prev_max > curr and curr < next_max: 
                units = min(prev_max, next_max) - curr 

            total = total + units

        return total
