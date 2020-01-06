class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        #use_dict_store key:nums[i],value:i

        #iteration to check (target-nums[i]) exists or not
        #if not, set table[nums[i]] = i
        #else, return [i, table[target-nums[i]]]

        table = {}
        for i, num in enumerate(nums):
            if (target-num) in table:
                return [i, table[target-num]]
            else:
                table[num] = i
        return []
        '''
        for i in range(len(nums) - 1):
            if (target - nums[i]) in nums[i+1:]:
                return [i, i+1+nums[i+1:].index(target-nums[i])]
        return []
        '''
