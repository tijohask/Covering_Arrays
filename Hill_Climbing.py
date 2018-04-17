import sys
import numpy
import random
import itertools
import time

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


#Code returns a 2D array, giving every row gotten by counting.
  #uses the input array as a base for its indices
#Example: 2,3,5
#Returns:
"""
 [0 0 0]
 [0 0 1]
 [0 0 2]
 [0 1 0]
 [0 1 1]
 [0 1 2]
 [1 0 0]
 [1 0 1]
 [1 0 2]
 [1 1 0]
 [1 1 1]
 [1 1 2]

"""
#General algorithm is to iteratively create all possible tuples up to the
#maximum value of the input array, then remove the ones that don't fit our
#established pattern.
def create_full_array(input_array):
  give = []
  for i in k_level:
    give.append(list(numpy.arange(i)))
  arr = []
  for i in itertools.product(*give):
    arr.append(list(i))
  return numpy.asarray(arr)

#Get every combination, check to make sure the right number of unique
  #interactions are in there.
  #If there are enough in all, then success!
  #else, false.
def check_interactions(test, k_level, num_inter):
  #get all existing combinations (interactions) from the data
  for p in itertools.combinations(numpy.arange(len(k_level)), num_inter):
    #Mul represents the number of unique iterations we expect for the exerpt
    mul = 1
    for i in p:
      mul = mul*k_level[i]
    #check if every possible interaction is represented
    if(numpy.unique(test[:,p], axis=0).shape[0] < mul):
      #if not, return false
      return False
  #if we made it through the whole for loop, return true
  return True

#Create an array with random, non-duplicate elements based on
#  The input array, and
#  The size given to the function
def create_test_array(array, size):
  #Sorted for readability
  #random.sample to prevent duplicate elements
  #min to make sure that we don't run into a sample error
  ii = sorted(random.sample(range(array.shape[0]), size))
  return array[ii,:]

def setup():
  #Take the system arguments
  #get the desired number of interactions
  num_inter = int(sys.argv[1])

  #get the array
  k_level = sys.argv[2]
  k_level = k_level.split(',')
  k_level = numpy.asarray(sorted(list(map(int, k_level))))

  print(k_level)
  print("Max Level: " + str(max(k_level)))
  print("Length of array: " + str(len(k_level)))
  
  return ( num_inter, k_level )

def create_cover(k_level, num_inter):
  full = create_full_array(k_level)
  cov_size = min( find_size( num_inter, len(k_level), max(k_level) ), full.shape[0] )

  running = 100
  test = []
  working_test = numpy.arange(0)

  while(running):
    #Create a new test array
    test = create_test_array(full, cov_size)
    #check if all interactions are represented in this test array
    if(check_interactions(test, k_level, num_inter)):
      #save the working test
      cov_size = cov_size - 1
      working_test = test
    else:
      #else, iterate down if we have a working test
      if(working_test.shape[0] != 0):
        running = running - 1
  
  return working_test

def mul_array(k_level):
  mul = 1
  for i in range(len(k_level)):
    mul = mul*k_level[i]
  return mul

#Recursively improve
def hill_climbing(pre_hill, k_level, num_inter):
  for i in range(len(pre_hill)):
    if(check_interactions(numpy.delete(pre_hill, i, 0), k_level, num_inter)):
      return hill_climbing(numpy.delete(pre_hill, i, 0), k_level, num_inter)
  return pre_hill

#END METHOD
#BEGIN CODE


start = time.process_time()

num_inter, k_level = setup()

pre_hill = create_cover(k_level, num_inter)

#print(find_size( num_inter, len(k_level), max(k_level) ))
print(pre_hill)
print(pre_hill.shape)
post_hill = hill_climbing(pre_hill, k_level, num_inter)
print(post_hill)
print(post_hill.shape)
print(mul_array(k_level))
#print(create_full_array(k_level))
end = time.process_time()
print("Elapsed Time: " + str(end - start))



