class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        [1,2,3,4,0,0,0]
        3
        [2,5,6]
        3
        """
        #forward_from_array_end_to_begin
        #compare_last_value_each_time
        #assign_max_value_to_array_end
        if n < 1:
            return 

        if m < 1:
            for i in range(n):
                nums1[i] = nums2[i]
            return

        i = m - 1
        j = n - 1
        while i >= 0 and j >=0:
            if nums1[i] <= nums2[j]:
                nums1[i+j+1] = nums2[j]
                j = j - 1
            else:
                nums1[i+j+1] = nums1[i]
                i = i - 1
        if j > 0:
            for jj in range(j,-1, -1):
                nums1[jj] = nums2[jj]
        if j == 0:
            nums1[i+1] = nums2[j]
