#!/usr/bin/env python3

import numpy as np
import re

main_file = open('main.sv').read()
match = re.search(r'parameter SAMPLE_DEPTH = (\d+);', main_file, re.U)
sample_depth = int(match.group(1))

print('SAMPLE_DEPTH = ', sample_depth, 'bits')

t = np.arange(0, 2**sample_depth-1, 1).astype(int)
s = (128 + np.sin(np.pi * t / (2**(sample_depth-4))) * 127).astype(int)
print('minval =', s.min())
print('maxval =', s.max())
print('samples = ', len(s))


with open('sine.mem', 'w') as sine_file:
    for i in s:
        hx = ('00' + hex(i)[2:])[-2:]
        print(hx, end=' ', file=sine_file)
    print(file=sine_file)
