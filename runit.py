#!/usr/bin/env python

import sys, os, subprocess
import os.path
import argparse
import time

def run_java(filename, extension, args):

    executable = filename[0:-len(extension)]
    
    cmd = "javac {} && java {} && rm {}.class".format(filename, executable, executable)
    
    run(cmd, extension, args)
    
def run_cs(filename, extension, args):
    
    # gerjo: search the unity hub path for the latest installation, instead of 
    # hardcoding paths here.
    
    compilers = [
        "/Users/gerjo/extern/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mcs",
        "/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mcs",
        "/Applications/Unity/Hub/Editor/2018.3.11f1/Unity.app/Contents/MonoBleedingEdge/bin/mcs",
    ]

    runtimes = [
        "/Users/gerjo/extern/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mono",
        "/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mono",
        "/Applications/Unity/Hub/Editor/2018.3.11f1/Unity.app/Contents/MonoBleedingEdge/bin/mono",
    ]
    
    compiler = runtime = None
    
    for bin in compilers:
        if os.path.isfile(bin):
            compiler = bin
            
    for bin in runtimes:
        if os.path.isfile(bin):
            runtime = bin
    
    if compiler == None or runtime == None:
        error(4, "Cannot run {} files. Either runtime or compiler isn't found.".format(extension))
    
    tmp = "out.exe";
    
    # Compile ...
    cmd = "{} -out:'{}' '{}'".format(compiler, tmp, filename)
    
    # ...and on success...
    cmd += " && "
    
    # ... execute and delete
    cmd += "({} '{}'; rm -f '{}')".format(runtime, tmp, tmp)
    
    run(cmd, extension, args)
    

recipes = {}

recipes[".cpp"] = "c++ -Wall -Wextra -std=c++14 {} -o out && (./out; rm ./out)"
recipes[".c"]   = "gcc -Wall -Wextra -std=c11 {} -o out && (./out; rm ./out)"
recipes[".js"]  = "node {}"
recipes[".php"] = "php {}"
recipes[".cs"]  = run_cs
recipes[".mm"]  = "clang++ -std=c++14 -ObjC++ -framework Foundation {} -o out && (./out; rm ./out)"
recipes[".r"]   = "/Library/Frameworks/R.framework/Resources/Rscript {}" 

recipes[".py"]  = "python3 {}"

recipes[".m"] = {
    "matlab": "matlab -nodisplay -nosplash -nodesktop -noFigureWindows -r \"try, run('{}'), catch e, fprintf('%s\\n', e.message), end;exit(0);\"",
    "objc":   "clang -framework Foundation {} -o out && (./out; rm ./out)"
}

recipes[".java"] = run_java


def error(code, str):
    sys.stderr.write(str + "\n")
    sys.exit(code) 
    
def run(cmd, extension, args):
    
    if args.bench:
        ruler = "----------------------"
        
        # Wrap in time, and use a custom format specifier to 
        # return the real time.
        cmd = "TIMEFORMAT='\n{0}\ntook %R seconds'; echo '{0}'; time {1}; unset TIMEFORMAT;".format(ruler, cmd)
    
    if args.entr:
        entr_cmd = "find .  -type f -name '*{}' -maxdepth {} |  entr -c -r sh -c '{}';"
        
        escaped_cmd = cmd.replace("'", "'\\''")
                
        os.system(entr_cmd.format(extension, args.maxdepth, escaped_cmd))
    
    else:
        os.system(cmd)
    
def main(args):

    filename = args.filename
    pwd = os.getcwd()
    
    extension = os.path.splitext(filename)[1].lower();

    if extension in recipes:
        recipe = recipes[extension]
        
        if type(recipe) == dict:
            
            if not args.recipe or args.recipe not in recipe:
                errormessage = "Multiple recipes known for file extension '{}'. Try one of these:\n".format(extension)
                
                for key in recipe:
                    errormessage += "  {} {} {}\n".format(os.path.basename(sys.argv[0]), key, filename)
                    
                error(3, errormessage)
                
            else:
                recipe = recipe[args.recipe]
            
        if callable(recipes[extension]):
            recipes[extension](filename, extension, args)
        else:
            run(recipe.format(filename), extension, args)
    else:
        error(2, "Cannot execute '{}' files. No known recipe.".format(extension))

parser = argparse.ArgumentParser(description="Execute any sort of file.", epilog="This ought to make it easier to quickly test something, right?")
parser.add_argument("recipe", help="The recipe to use in case file extension is ambiguous", nargs="?", default=None)
parser.add_argument("filename", help="The to be executed file")
parser.add_argument("--entr", help="Monitor for file changes", dest="entr", action="store_const", default=False, const=True)
parser.add_argument("--maxdepth", help="Recursion depth of find, in case entr is used", dest="maxdepth", action="store", default=2)
parser.add_argument("--nobench", help="Remote benchmark and ruler", dest="bench", action="store_const", default=True, const=True)

args = parser.parse_args()

main(args)

sys.exit(0)