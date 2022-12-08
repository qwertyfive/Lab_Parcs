from Pyro4 import expose
import random
import math

class Solver:
  def __init__(self, workers=None, input_file_name=None, output_file_name=None):
    self.input_file_name = input_file_name
    self.output_file_name = output_file_name
    self.workers = workers

  def solve(self):
    num_words = self.read_input()
    array_numbers = []
    for i in range(num_words):
      array_numbers.append(random.randint(1, 1000))
    step = num_words / len(self.workers)
    self.write_output(len(self.workers))
    mapped = []
    for i in range(0, len(self.workers)):
      mapped.append(self.workers[i].mymap(array_numbers[i*step : i*step + step]))
    reduced = self.myreduce(mapped)
    self.write_output(reduced)
    print("Job Finished")


  @staticmethod
  @expose
  def mymap(a): 
    max_number = a[0]
    for i in a:
        if(i>max_number):
           max_number = i
    return max_number


  @staticmethod
  @expose
  def myreduce(mapped):
    res = mapped[0].value
    for i in mapped:
      if(i.value > res):
          res = i.value
    return res
  
  def read_input(self):
    f = open(self.input_file_name, 'r')
    line = f.readline()
    f.close()
    return int(line)

  def write_output(self, output):
    f = open(self.output_file_name, 'a')
    f.write(str(output))
    f.write('\n')
    f.close()
