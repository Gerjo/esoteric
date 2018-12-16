#!/usr/bin/env python

import multiprocessing


def do_work(pair):
    return ["some result", "sub result", pair[0], pair[1]]


def main():
    num_workers = multiprocessing.cpu_count() * 2 - 1
    
    p = multiprocessing.Pool(num_workers)
    
    parameters = [
        [1, "hi"], 
        [2, "how"], 
        [3, "are you"]
    ]
    
    res = p.map(do_work, parameters)
    
    print(res)
    
    return 0


if __name__ == '__main__':
    exit(main())
    