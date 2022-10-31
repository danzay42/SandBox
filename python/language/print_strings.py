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

fin = "fin"
print(f"{fin:=^40}")