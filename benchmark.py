import types
import functools
import time

def make_benchmark(instance):
    """ 
    A primitive way to measure execution time of a python class instance. 
    Example usage below:
    
    # instantiate any class
    my_instance = widget()

    # Decorate the single instance
    make_benchmark(my_instance)

    # Call existing widget function
    my_instance.some_function()

    # will output the execution time of 'some_function'
    my_instance.print_benchmark_results()
    """
    
    
    class metadata:
        """ Stores some attributes pertaining to a benchmark result 
            for a given method. """
        
        # Method this meta instance pertains to
        method = None
        
        # Number of times method is invoked
        invoked = 0
        
        # Total execution time all invocations combined
        elapsed = 0
        
        # Most recent execution time
        delta = 0
        
        elapsed_squared = 0
        
        def __init__(self, method):
            self.method = method
    
    results = {}
    
    
    def print_benchmark_results():
        """ Print benchmark results so far, to the console. """
        print(get_benchmark_results())
        
    
    def get_benchmark_results():
        """ Retrieve a string representation of the benchmark results so far. """
        
        res = "{} timings:\n".format(instance.__class__.__name__)
    
        for name, meta in sorted(results.items(), key=lambda m: m[1].elapsed):
            if meta.invoked > 0:
            
                mean = meta.elapsed / meta.invoked
                stdev = pow((meta.elapsed_squared / meta.invoked) - (mean * mean), 0.5) 
            
                res += "  invocations: {:2d}".format(meta.invoked)
                res += ", avg: {:0.3f} sec".format(mean)
                res += " ({:0.3f} total)".format(meta.elapsed)
                res += ", {:0.3f} stdev".format(stdev)
                res += ", method: '{}'".format(name)
                res += "\n"
                
        return res
    
    def get_class_methods(type):
        """ Retrieve all callable functions in the given type. """
        
        attributes = [getattr(type, func) for func in dir(type)]
        return filter(lambda x: callable(x), attributes)
        
    
    def measure(fn, self, *args):
        """ Wrapper function that measures execution time of the given function. """
        
        meta = results[fn.__name__]
        meta.invoked += 1
        
        start = time.perf_counter()
        fn(*args)
        end = time.perf_counter()
        
        meta.delta = end - start
        
        meta.elapsed += meta.delta
        meta.elapsed_squared += pow(meta.delta, 2)
        
    for method in get_class_methods(instance):
        has_dict = hasattr(method, "__dict__")
        
        if has_dict:
            
            name = method.__name__
            setattr(instance, name, types.MethodType(functools.partial(measure, method), instance))
            
            results[name] = metadata(method)
            
    setattr(instance, "print_benchmark_results", print_benchmark_results)       
    setattr(instance, "get_benchmark_results", get_benchmark_results)       
    
    return instance
    
if __name__ == "__main__":      
    import random
    
    # Could be useful in the future to add this
    #def test_function(arg):
    #    print("test_function({})".format(arg))
    #    return arg
        
    #b = make_benchmark(test_function)
    #b.print_benchmark_results()
    #exit(0)
        
    class widget:
    
        bar = "foo"
    
        def __init__(self):
            #print("__init__")
            pass
        
        def wobble(self, magnitude):
            #print("Wobble({})".format(magnitude))
            time.sleep(random.uniform(0, .25))
        
        def dabble(self):
            #print("dabble - {0}".format(self.bar))
            pass
          
   
          
    w = widget()
    make_benchmark(w)

    w.wobble(10)
    w.wobble(10)
    w.wobble(10)
    w.wobble(10)
    w.dabble()
    w.dabble()
    w.dabble()
    w.dabble()

    w.print_benchmark_results()
    
