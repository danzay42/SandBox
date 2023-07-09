from math import pi, e, tau, inf

width = 40 

print("NumS".center(width, "="))
nums = [float("1"*width), float("1"*15), float("0." + "0" * 15 + "1"), 123e+5, -123e-5, pi, e, tau, inf]
for val in nums:
    print(f"{val:20.20}")

print(f"exponential".center(width, "="))
for val in nums:
    print(f"{val:e}")

print("procents".center(width, "="))
for val in [1,10,100,0.1,0.01]:
    print(f"{val:%}")

print("etc".center(width))
print("{:,.2f}".format(10001.23554))

print('-42'.zfill(6))
print('+42'.zfill(6))
print("{:0>6}".format(42))

print("www.example.com".strip('cmowz.'))

print(','.join(str(val) for val in [1, 2, 3, 4, 5, 6]))

print("vertical tabulation".center(width, "="))
print(*["one", "two", "three", 1,2,3,4,5], sep="\v")
print("escape_symbols".center(width, "="))
print("v1\v", "v2\v", "r1\r", "v3\v", "f1\f", "b1\b", "end1", "\b"*100, "end2", sep="")


fin = "fin"
print(f"{fin:=^40}")
