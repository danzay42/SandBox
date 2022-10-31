from typing import Dict, List
from collections import defaultdict

class Solution:
    
    def charCount(self, s: str) -> Dict:
        res = defaultdict(int)
        for ch in s:
            res[ch] += 1
        return res
    
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            #cc = self.charCount(s)
            cc = ''.join(sorted(s))
            res[cc] += [s]
        return res.values()
    
    def findAnagrams1(self, s: str, p: str) -> List[int]:
        res = []
        ang = self.charCount(p)
        for i in range(len(s)-len(p)+1):
            if ang == self.charCount(s[i:i+len(p)]):
                res.append(i)
        return res
    
    
    def findAnagrams2(self, s: str, p: str) -> List[int]:
        res = []
        if len(p) > len(s):
            return res
        
        ang = defaultdict(int)
        for ch in p: 
            ang[ch] += 1

        for i in range(len(p)-1):
            if s[i] in ang: 
                ang[s[i]] -= 1
            
        for i in range(-1, len(s)-len(p)+1):
            if i > -1 and s[i] in ang:
                ang[s[i]] += 1
            if i+len(p) < len(s) and s[i+len(p)] in ang: 
                ang[s[i+len(p)]] -= 1
                
            if not any(ang.values()): 
                res.append(i+1)
                
        return res



if __name__ == "__main__":
    a = 'a'*20001
    b = 'a'*10000
    res = Solution().findAnagrams2(a, b)
    print(res)
