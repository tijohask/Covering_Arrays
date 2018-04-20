import sys
import numpy
import itertools
import time
import random

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
#Example: 2,2,3
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
#General algorithm is to use itertools [behaving like nested for loops]
#to iteratively create every row in the product
def create_full_array(input_array):
  give = []
  for i in input_array:
    give.append(list(numpy.arange(i)))
  arr = []
  for i in itertools.product(*give):
    arr.append(list(i))
  return numpy.asarray(arr)


#Get every combination, check to make sure the right number of unique
  #interactions are in there.
  #If there are enough in all, then success!
  #else, false.
def greedy_generation(full, k_level, num_inter):
  #Start our algorithm off with the first row declared.
  #If we didn't do this, the for loop would declare it anyway.
  cur = numpy.asarray([full[0,:]])
  full = numpy.delete(full, 0, 0)

  #We know that 
    #len(covering array) <= len(full array)
  #So declare that we will run through the full array
  for x in range(full.shape[0]):
    #Declare an array of zeros equal in size to our full array.
    buckets = [0]*full.shape[0]
    
    #get all existing combinations (interactions) from the data
    for p in itertools.combinations(numpy.arange(len(k_level)), num_inter):
      
      #If check contains the interaction, then buckets will not increment
      check = numpy.unique(cur[:,p], axis=0)
      #If numpy.unique shows that all interactions have been applied,
      #Then do nothing
      mul = 1
      for i in p:
        mul = mul * k_level[i]
      
      #if all interactions of a specific slice have been found, then do nothing
      if(mul == len(check)):
        continue
      
      #
      for i in range(full.shape[0]):
        #print((check == full[i,p]).any(1))
        #print(full[i,p])
        buckets[i] = buckets[i] + int( not (check == full[i,p]).all(1).any() )
        #print(not (check == full[i,p]).all(1).any())

    #If all interactions are accounted for, then return what we have
    if(max(buckets) == 0):
      return cur
    
    #Else,
    #Find the first and largest value of buckets
    idx = buckets.index(max(buckets))
    
    #Append the associated value to cur
    cur = numpy.append(cur, [full[idx]], axis=0)
    
    #And delete the associated value from full
    full = numpy.delete(full, idx, 0)

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

def create_cover(k_level, num_inter):
  full = create_full_array(k_level)
  cov_size = min( find_size( num_inter, len(k_level), max(k_level) ), full.shape[0] )

  running = 100
  test = []
  working_test = numpy.arange(0)

  while(True):
    #Create a new test array
    test = create_test_array(full, cov_size)
    #check if all interactions are represented in this test array
    if(check_interactions(test, k_level, num_inter)):
      #save the working test
      #cov_size = cov_size - 1
      working_test = test
      break
    else:
      #else, iterate down if we have a working test
      running = running - 1
      if(running == 0):
        cov_size = min(mul_array(k_level), cov_size+1)
        running = 100
  
  return working_test

#END METHOD
#BEGIN CODE

start = time.process_time()
#Take the system arguments
#get the desired number of interactions
num_inter = int(sys.argv[1])

#get the array
k_level = sys.argv[2]
k_level = k_level.split(',')
k_level = numpy.asarray(sorted(list(map(int, k_level))))

full = create_full_array(k_level)
random = create_cover(k_level, num_inter)
greedy_array = greedy_generation(random, k_level, num_inter)
for x in range(greedy_array.shape[1], 0, -1):
  greedy_array = greedy_array[numpy.argsort(greedy_array[:,x-1], kind='mergesort')]
print(random)
print(random.shape)

print(greedy_array)
print(greedy_array.shape)
end = time.process_time()
print("Elapsed Time: " + str(end - start))

print(full.shape)
end = time.process_time()
print("Elapsed Time: " + str(end - start))


