def tcv_to_json(file: str):
    res = []
    with open(file) as fd:
        keys = fd.readline().strip().split('\t')
        res.extend([{
            k: v 
                for k, v in zip(keys, vals.strip().split('\t'))} 
                    for vals in fd.readlines()
                    ])
    return res

def spell_check(s1: str, s2: str):
    err, i, j = 0, len(s1), len(s2)

    while i and j:  
        i -= 1
        j -= 1
        if s1[i] != s2[j]:
            if (err:= err + 1) == 2:
                return False
            if i > j:
                j += 1
            elif j > i:
                i += 1

    err += i or j
    return err < 2


if __name__ == "__main__":
    print(tcv_to_json("step_one.tcv"))
    
    for ss in (("cat", "cat"), ("cat", "bat"), ("cat", "cab"), ("cbb", "cat"), ("", "a"), ("", ""), ("abcd", "bcd"), ("bcda", "bcd"), ("bcad", "bcd"), ("aabd", "abcd"), ("a`abcd", "bcd")):
        res = spell_check(*ss)
        print(ss, res)
