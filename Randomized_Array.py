import sys
import numpy
import random
import itertools
from itertools import combinations

#Found on stack overflow
def choose(n, k):
  """
  A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
  """
  if 0 <= k <= n:
    ntok = 1
    ktok = 1
    for t in range(1, min(k, n - k) + 1):
      ntok *= n
      ktok *= t
      n -= 1
    return ntok // ktok
  else:
    return 0

#Mathematically proven that the size of the covering array will be no larger
#than what is returned by this function
def find_size(t, k, v):
  top =  numpy.log(choose(k, t)) + (t * numpy.log(v))
  bottom = numpy.log( (v**t) / (v**t - 1) )
  return int( top / bottom ) + 1 

#Create an array with random, non-duplicate elements based on
#  The input array, and
#  The size given to the function
def create_test_array(array, size):
  #Sorted for readability
  #random.sample to prevent duplicate elements
  #min to make sure that we don't run into a sample error
  ii = sorted(random.sample(range(array.shape[0]), min(size, array.shape[0])))
  return array[ii,:]

def create_full_array(size, levels):
  arr = []
  for i in itertools.product(numpy.arange(levels), repeat=size):
    arr.append(list(i))
  return numpy.asarray(arr)

#Get every combination, check to make sure the right number of unique
  #elements are in there.
  #If there are enough in all, then success!
  #else, false.
def check_interactions(data, num_inter, num_level):
  #get all existing combinations (interactions) from the data
  for p in combinations(numpy.arange(data.shape[1]), num_inter):
    #check if every possible interaction is represented
    if(numpy.unique(data[:,p], axis=0).shape[0] < num_level**num_inter):
      #if not, return false
      return False
  #if we made it through the whole for loop, return true
  return True

num_inter = int(sys.argv[1])
num_k = int(sys.argv[2])
num_level = int(sys.argv[3])

full = create_full_array(num_k, num_level)
cov_size = find_size(num_inter, num_k, num_level)

running = 100
test = []
working_test = numpy.arange(0)

while(running > 0):
  #Create a new test array
  test = create_test_array(full, cov_size)
  #check if all interactions are represented in this test array
  if(check_interactions(test, num_inter, num_level)):
    #if they are, reduce the covariance size and try again
    cov_size = cov_size - 1
    #also save the working test
    working_test = test
  else:
    #else, the iterations if we have a working test
    if(working_test.shape[0] != 0):
      running = running - 1
print(working_test)
print(working_test.shape)




