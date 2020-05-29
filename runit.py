#!/usr/bin/env python3

import sys, os, subprocess
import os.path, fnmatch
import argparse
import time

def get_sub_args(args):
    return " ".join(args.args)

def run_java(filename, extension, args):

    executable = filename[0:-len(extension)]
    
    cmd = "javac {} && java {} {} && rm {}.class".format(filename, executable, get_sub_args(args), executable)
    
    run(cmd, extension, args)
    
def find_cs_binaries():
    roots = [
        "/Applications/Unity/Hub/Editor/",
        
        # Non unity hub installations
        "/Applications/Unity/"
    ]
    
    # Only "MonoBleedingEdge" seems to work.
    compiler_executable = "*/MonoBleedingEdge/bin/mcs"
    runtime_executable = "*/MonoBleedingEdge/bin/mono"
    
    compiler = runtime = None
    
    for root in roots:
        for subroot, dirnames, filenames in os.walk(root):
            for candidate in filenames:
                candidate = os.path.join(subroot, candidate) 
                
                if fnmatch.fnmatch(candidate, compiler_executable):
                    compiler = candidate
                    
                if fnmatch.fnmatch(candidate, runtime_executable):
                    runtime = candidate
                    
                # early out
                if compiler != None and runtime != None: 
                    return (compiler, runtime)
                    
    return (compiler, runtime)
    
def run_cs(filename, extension, args):
    
    compiler, runtime = find_cs_binaries()
    
    if compiler == None or runtime == None:
        error(4, "Cannot run '{}' files. Either runtime or compiler isn't found.".format(extension))
    
    
    tmp = "out.exe";
    
    # Compile ...
    cmd = "{} -out:'{}' '{}'".format(compiler, tmp, filename)
    
    # ...and on success...
    cmd += " && "
    
    # ... execute and delete
    cmd += "({} '{}' {}; rm -f '{}')".format(runtime, tmp, get_sub_args(args), tmp)
    
    run(cmd, extension, args)
    

recipes = {}

# 
#recipes[""] = {
#    "cordova": "cordova prepare browser"
#}

recipes["cpp"] = "c++ -Wall -Wextra -std=c++14 {source} -o out && (./out {args}; rm ./out)"
recipes["c"]   = "gcc -Wall -Wextra -std=c11 {source} -o out && (./out {args}; rm ./out)"
recipes["js"]  = "node {source} {args}"
recipes["scpt"]  = "osascript {source} {args}"
recipes["php"] = "php {source} {args}"
recipes["cs"]  = run_cs
recipes["sh"]  = "sh {source} {args}"
recipes["bash"]  = "bash {source} {args}"
recipes["zsh"]  = "zsh {source} {args}"
recipes["mm"]  = "clang++ -std=c++14 -ObjC++ -framework Foundation {source} -o out && (./out {args}; rm ./out)"
recipes["r"]   = "/Library/Frameworks/R.framework/Resources/Rscript {source} {args}" 

recipes["py"]  = "python3 {source} {args}"

recipes["matlab"] = "matlab -nodisplay -nosplash -nodesktop -noFigureWindows -r \"try, run('{source}'), catch e, fprintf('%s\\n', e.message), end;exit(0);\""
recipes["objc"] = "clang -framework Foundation {source} -o out && (./out {args}; rm ./out)"


recipes["m"] = ["matlab", "objc"]

recipes[".java"] = run_java

def error(code, str):
    sys.stderr.write(str + "\n")
    sys.exit(code) 
    
def run(cmd, extension, args):
    
    #print(cmd)
    #exit(0)
    
    if args.bench:
        ruler = "----------------------"
        
        # Wrap in time, and use a custom format specifier to 
        # return the real time.
        cmd = "TIMEFORMAT=\"\n{0}\ntook %R seconds starting at $(date +'%T')\"; echo '{0}'; time {1}; unset TIMEFORMAT;".format(ruler, cmd)
    
    if args.entr:
        entr_cmd = "find . -type f -name '*{}' -maxdepth {} |  entr -c -r sh -c '{}';"
        
        escaped_cmd = cmd.replace("'", "'\\''")
                
        os.system(entr_cmd.format(extension, args.maxdepth, escaped_cmd))
    
    else:
        os.system(cmd)
    
def main(args):

    filename = args.filename
    pwd = os.getcwd()
   
    extension = os.path.splitext(filename)[1].lower().lstrip(".")
   
    # Use explicitly defined recipe when provided
    if args.recipe:
        recipe = args.recipe
        
    # otherwise deduce it from file extension
    elif extension is not "":
        recipe = extension
    else:
        recipe = None
        
    if recipe in recipes:
        
        # Ambiguous recipe. List the alternatives
        if isinstance(recipes[recipe], list):
            errormessage = "recipe '{}' is ambigious, try the following:\n".format(recipe);
            
            for key in recipes[recipe]:
                errormessage += "  {} {} {} [args...]\n".format(os.path.basename(sys.argv[0]), key, filename)
            
            error(3, errormessage)
        
        # Fancy recipe, requires helper code to run    
        elif callable(recipes[recipe]):
            recipes[recipe](filename, extension, args)
            
        # Execute recipe based on a string    
        else:
            run(recipes[recipe].format(source=filename, args=get_sub_args(args)), extension, args)
            
    else:
        error(2, "Cannot execute '{}' files. No known recipe.".format(recipe))
    
        
parser = argparse.ArgumentParser(description="Execute any sort of file.", epilog="This ought to make it easier to quickly test something, right?")
parser.add_argument("recipe", help="The recipe to use in case file extension is ambiguous", nargs="?", default=None)
parser.add_argument("filename", help="The to be executed file")
parser.add_argument("--entr", help="Monitor for file changes", dest="entr", action="store_const", default=False, const=True)
parser.add_argument("--maxdepth", help="Recursion depth of find, in case entr is used", dest="maxdepth", action="store", default=2)
parser.add_argument("--nobench", help="Remote benchmark and ruler", dest="bench", action="store_const", default=True, const=True)
parser.add_argument('args', nargs='*', default=None, help="Arguments passed onto the executed file")

args = parser.parse_args()

main(args)

sys.exit(0)
