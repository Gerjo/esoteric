#!/usr/bin/env python

import numpy as np
import sys
import os
import scipy.io

if len(sys.argv) < 2:
    sys.exit("Expected one argument.")

matfilepath = sys.argv[1]

if not os.path.isfile(matfilepath):
    sys.exit("Input mat file does not exist.")
    
mat = scipy.io.loadmat(matfilepath)

# Dump the whole thing
print(mat)

print("")
print("Summary:")

for key in mat:
    value = mat[key]
    
    arr = np.array(value)
    
    if hasattr(value, "shape"):
        print("{} = shape{}".format(key, arr.shape))
    else:
        print("{} = {}".format(key, value))