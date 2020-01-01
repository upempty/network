#leet code 26
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        #sort the array
        #nums.sort() 
        #Note: nums=sorted(nums) issue

        #get first element index
        i = 0

        #use array index from 2th increasing compare
        for j in range(1, len(nums)):
            if nums[i] != nums[j]:
                i += 1
                #Note: can't use nums[++i] issue
                nums[i] = nums[j]
        return i+1
