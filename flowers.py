"""
You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty, and an integer n, return true if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule and false otherwise.



Example 1:

Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
Example 2:

Input: flowerbed = [1,0,0,0,1], n = 2
Output: false
"""

tests = (
    (([1, 0, 0, 0, 1], 1), True),
    (([1, 0, 0, 0, 1], 2), False),
)

from typing import List


class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        for i in range(len(flowerbed)):
            if n == 0:
                break
            if flowerbed[i] == 0:
                if (i == 0 or flowerbed[i-1] == 0) and (i == len(flowerbed) - 1 or flowerbed[i+1] == 0):
                    n -= 1
                    flowerbed[i] = 1
        return n == 0


if __name__ == "__main__":
    s = Solution()
    for test in tests:
        out = s.canPlaceFlowers(*test[0])
        print(f"Test - {test[0]}\nOutput - {out}\nResult - {test[1] == out}")
