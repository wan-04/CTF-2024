#!/usr/bin/env python3
import qiling
from qiling.const import QL_VERBOSE
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <ELF>")
        sys.exit(1)
    cmd = [sys.argv[1]]
    ql = qiling.Qiling(cmd, console=False, rootfs='.', verbose=QL_VERBOSE.OFF)
    ql.debugger = True
    ql.debugger = "gdb:127.0.0.1:9999"
    ql.run()