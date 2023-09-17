#!/usr/bin/env python3
from header import *

if __name__ == "__main__":
    if matrix == 1:
        from src_1x2x6.app_core import MatrixApplication
    elif matrix == 2:
        from src_4x36.app_core import MatrixApplication
    elif matrix == 3:
        from src_1x36.app_core import MatrixApplication
    elif matrix == 4:
        from src_1x2x2.app_core import MatrixApplication
    elif matrix == 5:
        from src_4x18.app_core import MatrixApplication
    core = MatrixApplication()
    sys.exit(core.exec_())
