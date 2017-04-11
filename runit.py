#!/usr/bin/env python3

import sys, os, subprocess
import os.path

recipes = {}

recipes[".cpp"] = "c++ -Wall -Wextra -std=c++14 {} -o out && ./out && rm ./out"
recipes[".c"]   = "gcc -Wall -Wextra -std=c11 {} -o out && ./out && rm ./out"
recipes[".js"]  = "node {}"
recipes[".py"]  = "python {}"
recipes[".php"] = "php {}"
recipes[".m"]   = "clang -framework Foundation {} -o out && ./out && rm ./out"
recipes[".mm"]  = "clang++ -std=c++14 -ObjC++ -framework Foundation {} -o out && ./out && rm ./out"

def error(code, str):
    sys.stderr.write(str + "\n")
    sys.exit(code) 

def run(cmd):
    os.system(cmd)

if len(sys.argv) == 2:
    filename = sys.argv[-1]
    pwd = os.getcwd()
    
    #if os.access(filename, os.X_OK):
    #    run(filename)
    #else:
    extension = os.path.splitext(filename)[1].lower();
    
    if extension in recipes:
        run(recipes[extension].format(filename))
    else:
        error(2, "Cannot execute '{}' files. No known recipe.".format(extension))
    
else:
    error(1, "Unknown number of arguments specified: {}".format(len(sys.argv)))

sys.exit(0)