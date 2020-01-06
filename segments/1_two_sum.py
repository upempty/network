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
