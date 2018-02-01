#!/usr/bin/env python

import sys, os, subprocess
import os.path

def run_cs(filename):
    compilers = [
        "/Users/gerjo/extern/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mcs",
        "/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mcs",
    ]

    runtimes = [
        "/Users/gerjo/extern/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mono",
        "/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mono",
    ]
    
    compiler = runtime = None
    
    for bin in compilers:
        if os.path.isfile(bin):
            compiler = bin
            
    for bin in runtimes:
        if os.path.isfile(bin):
            runtime = bin
    
    if compiler == None or runtime == None:
        print("Cannot run .cs files. Either runtime or compiler isn't found.")
        return
    
    tmp = "out.exe";
    
    didCompile = run("{} -out:{} {}".format(compiler, tmp, filename))
        
    # Test for success exit code
    if didCompile == 0:
        run("{} {}".format(runtime, tmp))
        run("rm -f {}".format(tmp))

recipes = {}

recipes[".cpp"] = "c++ -Wall -Wextra -std=c++14 {} -o out && ./out && rm ./out"
recipes[".c"]   = "gcc -Wall -Wextra -std=c11 {} -o out && ./out && rm ./out"
recipes[".js"]  = "node {}"
recipes[".py"]  = "python {}"
recipes[".php"] = "php {}"
recipes[".cs"]  = run_cs
recipes[".m"]   = "clang -framework Foundation {} -o out && ./out && rm ./out"
recipes[".mm"]  = "clang++ -std=c++14 -ObjC++ -framework Foundation {} -o out && ./out && rm ./out"

def error(code, str):
    sys.stderr.write(str + "\n")
    sys.exit(code) 

def run(cmd):
    return os.system(cmd)

if len(sys.argv) == 2:
    filename = sys.argv[-1]
    pwd = os.getcwd()
    
    # Execute as-is (disabled - seems confusing)
    #if os.access(filename, os.X_OK):
    #    run("./" + filename)
    #else:
    
    extension = os.path.splitext(filename)[1].lower();

    if extension in recipes:
        recipe = recipes[extension]
        
        if callable(recipes[extension]):
            recipes[extension](filename)
        else:
            run(recipe.format(filename))
    else:
        error(2, "Cannot execute '{}' files. No known recipe.".format(extension))
    
else:
    error(1, "Unknown number of arguments specified: {}".format(len(sys.argv)))

sys.exit(0)