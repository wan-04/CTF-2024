#!/usr/bin/python3 -u

import subprocess
import tempfile
import base64
import sys

with tempfile.NamedTemporaryFile() as f:
    try:
        num_bytes = int(input('How many bytes is your base64-encoded exploit? '))
        if num_bytes > 2**20:
            print('Too big')
            exit(0)

        print('Exploit as base64 please')
        data = base64.b64decode(sys.stdin.buffer.read(num_bytes))

        f.write(data)
        f.flush()

        print('TURN UP THE HEAT!')
        subprocess.check_call(['/home/user/d8', '--sandbox-testing', f.name])
    except:
        print('Its gettin cold in here...')
