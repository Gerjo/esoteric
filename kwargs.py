
def format(string, **args):
    d = dict()
    d["a"] = "A";
    d["b"] = "B";
    
    return string.format(**args, **d)
    
print(format("test {a} and example {name} {size}", name="potato", size="xl"))