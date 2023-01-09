# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
def guess(num: int) -> int:
    return 1

class Solution:
    def guessNumber(self, n: int) -> int:
        f, t = 1, n
        while f <= t:
            g = (f+t)//2
            res = guess(g)
            if res==0:
                return g
            elif res==1:
                f = g + 1
            else:
                t = g - 1
        return -1

