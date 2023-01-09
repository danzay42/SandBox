from collections import deque, defaultdict


class Solution:
    def isValid(self, s: str) -> bool:
        parentheses = {k: v for k, v in ('()', '{}', '[]')}
        res = deque()
        for p in s:
            if p in parentheses:
                res.append(parentheses[p])
                continue
            elif res and res.pop() == p:
                continue
            return False
        return not res


if __name__ == "__main__":
    res = Solution().isValid("()[{}")
    print(res)
