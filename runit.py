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
recipes[".mm"]  = "clang++ -std=c++14 -ObjC++ -framework Foundation {} -o out && ./out && rm ./out"

#recipes[".m"]   = 

recipes[".m"] = {
    "matlab": "matlab -nodisplay -nosplash -nodesktop -noFigureWindows -r \"try, run('{}'), catch e, fprintf('%s\\n', e.message), end;exit(0);\"",
    "objc":   "clang -framework Foundation {} -o out && ./out && rm ./out"
}

#C:\<a long path here>\matlab.exe" -nodisplay -nosplash -nodesktop -r "try, run('C:\<a long path here>\mfile.m'), catch me, fprintf('%s / %s\n',me.identifier,me.message), end, exit"

def error(code, str):
    sys.stderr.write(str + "\n")
    sys.exit(code) 

def run(cmd):
    return os.system(cmd)

if len(sys.argv) >= 2:
    filename = sys.argv[-1]
    pwd = os.getcwd()
    
    if os.access(filename, os.X_OK):
        run("./" + filename)
    else:
        extension = os.path.splitext(filename)[1].lower();
    
        if extension in recipes:
            recipe = recipes[extension]
            
            if type(recipe) == dict:
                
                if len(sys.argv) <= 2 or sys.argv[1] not in recipe:
                    errormessage = "Multiple recipes known for file extension '{}'. Try one of these:\n".format(extension)
                    
                    for key in recipe:
                        errormessage += "  {} {} {}\n".format(sys.argv[0], key, filename)
                        
                    error(3, errormessage)
                    
                else:
                    subrecipe = sys.argv[1]
                    recipe = recipe[subrecipe]
            
            if callable(recipes[extension]):
                recipes[extension](filename)
            else:
                run(recipe.format(filename))
        else:
            error(2, "Cannot execute '{}' files. No known recipe.".format(extension))
    
else:
    error(1, "Unknown number of arguments specified: {}".format(len(sys.argv)))

sys.exit(0)