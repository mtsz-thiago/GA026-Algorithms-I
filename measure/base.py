from time import time
from typing import Any, List
from numpy.random import randint
from tqdm import tqdm

class DummyCaller():
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return None

class ExecutionResult:
    elapsed: int
    output_data: Any

class SortAssertion():
    #TODO generalize implementation for descending order
      
    def __call__(self, input_data, instance_executions: List[ExecutionResult], verbose=False) -> Any:
        for (exp, (input_d, output)) in enumerate(zip(input_data, instance_executions)):
            
            # assert size match
            assert len(input_d) == len(output.output_data), f"input {input_d} size mismatch output {output.output_data} for experiment #{exp}"

            # assert ascending order
            for i in range(0, len(input_d)-1):
                assert output.output_data[i] <= output.output_data[i+1],  f"output {output.output_data} not sorted properly for experiment #{exp}"
                
            # assert elements match
            assert set(input_d) == set(output.output_data), f"output {output.output_data} has elements not in {input_d} for experiment #{exp}"
            

class ListDataGenerator():
    
    def __init__(self, key_generator = randint, max_instance_sz = 100, lower = 0, upper = 100):
        self.key_generator = key_generator
        self.max_instance_sz = max_instance_sz
        self.lower = lower 
        self.upper = upper
    
    def __call__(self, sample_sz: int, verbose = False):
        
        instances_sizes = randint(1,self.max_instance_sz, sample_sz)
        
        full_sample = self.key_generator( 
                                  self.lower, 
                                  self.upper, 
                                 size=(sample_sz, self.max_instance_sz))
        
        if verbose:
            print(f"generating data sample with {sample_sz} instances")
            data = [l[0:s] for l,s in tqdm(zip(full_sample, instances_sizes))]
        else:    
            data = [l[0:s] for l,s in zip(full_sample, instances_sizes)]
        
        return data
        

class ExperimentExecuter():
    
    def __init__(self, function, data_generator, data_regressor, correctness_verifier = None):
      self.function = function  
      self.data_factory = data_generator  
      self.data_regressor = data_regressor
      self.correctness_verifier = correctness_verifier  

    def execute_instance(self, data, verbose):
        start = time()
        output_data = self.function(data.copy(), verbose)
        end = time()
        r = ExecutionResult()
        r.elapsed = end - start
        r.output_data = output_data
        return r

    def execute(self, sample_sz:int = None, verbose = True):
        
        instance_executions = [(self.execute_instance(d, verbose),sz) for d, sz in self.data_factory.gen()]
        
        regression = self.data_regressor(input_data, instance_executions, verbose)
        
        return regression, input_data, instance_executions
        

if __name__ == "__main__":
    pass