#!/usr/bin/env python3

import sys, os, subprocess
import os.path, fnmatch
import argparse
import time

def get_recipes():
    """Return all known recipes of this program"""
    return [
        {
            "recipe": "cpp",
            "ext": [".cpp", ".h"],
            "run": "c++ -Wall -Wextra -std=c++14 {source} -o out && (./out {args}; rm ./out)"
        },
        {
            "recipe": "c",
            "ext": [".c", ".h"],
            "run": "gcc -Wall -Wextra -std=c11 {source} -o out && (./out {args}; rm ./out)"
        },
        {
            "recipe": "javascript",
            "ext": [".js"],
            "run": "node {source} {args}"
        },
        {
            "recipe": "osascript",
            "ext": [".scpt"],
            "run": "osascript {source} {args}"
        },
        {
            "recipe": "php",
            "ext": [".php"],
            "run": "php {source} {args}"
        },
        {
            "recipe": "cs",
            "ext": [".cs"],
            "run": run_cs
        },
        {
            "recipe": "sh",
            "ext": [".sh"],
            "run": "sh {source} {args}"
        },
        {
            "recipe": "bash",
            "ext": [".bash"],
            "run": "bash {source} {args}"
        },
        {
            "recipe": "zsh",
            "ext": [".zsh"],
            "run": "zsh {source} {args}"
        },
        {
            "recipe": "objc++",
            "ext": [".mm"],
            "run": "clang++ -std=c++14 -ObjC++ -framework Foundation {source} -o out && (./out {args}; rm ./out)"
        },
        {
            "recipe": "r",
            "ext": [".r"],
            "run": "/Library/Frameworks/R.framework/Resources/Rscript {source} {args}" 
        },
        {
            "recipe": "npm",
            "ext": [".js", ".html", ".css"],
            "run": "npm start --prefix {source}"
        },
        {
            "recipe": "python",
            "ext": [".py", ".py3"],
            "run": "python3 {source} {args}"
        },
        {
            "recipe": "matlab",
            "ext": [".m"],
            "run": "matlab -nodisplay -nosplash -nodesktop -noFigureWindows -r \"try, run('{source}'), catch e, fprintf('%s\\n', e.message), end;exit(0);\""
        },
    	{
            "recipe": "objc",
            "ext": [".m"],
            "run": "clang -framework Foundation {source} -o out && (./out {args}; rm ./out)"
        },
        {
            "recipe": "java",
            "ext": [".java"],
            "run": run_java
        },
    ]

def get_sub_args(args):
    return " ".join(args.args)

def run_java(filename, recipe, args):
    """Execute a java source code file"""
    
    # Java uses the file's name to determine the entry point.
    executable = os.path.splitext(filename)[0]
    
    cmd = "javac {} && java {} {} && rm {}.class".format(filename, executable, get_sub_args(args), executable)
    
    run(cmd, recipe, args)
    
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
    
def run_cs(filename, recipe, args):
    
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
    
    run(cmd, recipe, args)


def error(code, str):
    sys.stderr.write(str + "\n")
    sys.exit(code) 
    
def execute_recipe(recipes, filename, args):
    
    if len(recipes) == 1:
        recipe = recipes[0]
        
        # Fancy recipe, requires helper code to run    
        if callable(recipe["run"]):
            recipe["run"](filename, recipe, args)
        
        # Execute recipe based on a string
        else:
            run(recipe["run"].format(source=filename, args=get_sub_args(args)), recipe, args)
    else:
        errormessage = "recipe is ambigious, try one of the following:\n";
        
        for r in recipes:
            errormessage += "  {} {} {} [args...]\n".format(os.path.basename(sys.argv[0]), r["recipe"], filename)
        
        error(3, errormessage)
        
def run(cmd, recipe, args):

    if args.bench:
        ruler = "----------------------"
        
        # Wrap in time, and use a custom format specifier to 
        # return the real time.
        cmd = "TIMEFORMAT=\"\n{0}\ntook %R seconds starting at $(date +'%T')\"; echo '{0}'; time ({1}); unset TIMEFORMAT;".format(ruler, cmd)
    
    if args.entr:
        entr_cmd = "find . -type f {} -maxdepth {} |  entr -c -r sh -c '{}';"
        pattern = ""
        
        for i, ext in enumerate(recipe["ext"]):
            
            if i > 0:
                pattern += "-o "
            
            pattern += "-name '*{}' ".format(ext)
        
        escaped_cmd = cmd.replace("'", "'\\''")
                
        os.system(entr_cmd.format(pattern, args.maxdepth, escaped_cmd))
    
    else:
        os.system(cmd)
    
# TODO: gerjo: this could be part of the recipe setup. Specify which 
# files to sense for in order to deduce how to execute a path.  
def deduce_recipes_from_path(path):
    
    # Node projects have a package file.
    if os.path.isfile(os.path.join(path, "package.json")):
        return [r for r in get_recipes() if r["recipe"] == "npm"]
    
    return []
    
def main(args):

    filename = args.filename
    pwd = os.getcwd()
   
    extension = os.path.splitext(filename)[1].lower()
   
    # Use explicitly defined recipe when provided
    if args.recipe:
        recipes = [r for r in get_recipes() if r["recipe"] == args.recipe]
        
        if len(recipes) > 0:
            execute_recipe(recipes, filename, args)
        else:
            error(7, "Requested recipe '{}' does not exist.".format(args.recipe))
        
    # otherwise deduce it from file extension
    elif extension is not "":
        recipes = [r for r in get_recipes() if extension in r["ext"]]
    
        if len(recipes) > 0:
            execute_recipe(recipes, filename, args)
        else:
            error(8, "No recipe available for file extension '{0}'.".format(extension))
       
    # Deduce it from path    
    elif os.path.isdir(filename):
        recipes = deduce_recipes_from_path(filename)
    
        if len(recipes) > 0:
            execute_recipe(recipes, filename, args)
        else:
            error(6, "Cannot determine recipe based on path '{}'.".format(filename))
            
    # This code shouldn't normally be reached
    else:
        error(2, "Cannot execute '{}'. No known recipe could be deduced.".format(filename))   
        
        
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
