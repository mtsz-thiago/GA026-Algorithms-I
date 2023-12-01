import time
import resource
import os
import psutil
 
# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

from dataclasses import dataclass

@dataclass
class PerformanceMeasure:
    elapsed_time: float
    cpu_time: float
    memory_usage: float
    input_V: int = None
    input_E: int = None
    output_V: int = None
    output_E: int = None
    root_node: int = None

def measure_performance(func, verbose=False):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_resources = resource.getrusage(resource.RUSAGE_SELF)
        mem_before = process_memory()

        result = func(*args, **kwargs)

        mem_after = process_memory()
        end_time = time.time()
        end_resources = resource.getrusage(resource.RUSAGE_SELF)

        elapsed_time = 1000*(end_time - start_time)
        cpu_time = 1000*(end_resources.ru_utime - start_resources.ru_utime)
        memory_usage = mem_after - mem_before
        measure = PerformanceMeasure(elapsed_time, cpu_time, memory_usage)

        g = args[0]
        measure.input_E = g.get_num_edges()
        measure.input_V = g.get_num_vertices()
        measure.output_E = result.get_num_edges()
        measure.output_V = result.get_num_vertices()
        measure.root_node = args[1]
        
        if verbose:
            print(f"Elapsed Time: {elapsed_time} seconds")
            print(f"CPU Time: {cpu_time} seconds")
            print(f"Memory Usage: {memory_usage} bytes")

        return result, measure

    return wrapper


if __name__ == '__main__':
    pass