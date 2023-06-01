class Solution:
    values = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    def romanToInt(self, s: str) -> int:
        sum = 0
        for temp in s[::-1]:
            if sum and self.values[temp] < sum:
                sum -= self.values[temp]
            else:
                sum += self.values[temp]
        return sum


if __name__ == "__main__":
    sol = Solution()
    print(sol.romanToInt("MCMXCIV"))
