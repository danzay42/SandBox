# keywords arguments
def fn1(a,b,*,c,d):
    pass

fn1(1,1, c=10, d=10)      # ok
# fn1(1,1, 10, 10)        # error
fn1(1,b=1, c=10, d=10)    # ok

# positional arguments
def fn2(a,b,/,c,d):
    pass

# fn2(1,b=1,c=1,d=1)      # error
fn2(1,1,c=1,d=1)          # ok
fn2(1,1,1,1)              # ok

import warnings

warnings.warn("test message")


print("end of file")