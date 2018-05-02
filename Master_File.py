import sys
import numpy
import random
import itertools
import time

###############################################################
#Begin methods for randomized array generation
###############################################################

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
  ii = sorted(random.sample(range(array.shape[0]), size))
  return array[ii,:]

#Create a covering array by putting together random rows from the 
#full array and checking whether they form a covering array.
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
      #else, iterate down
      running = running - 1
      #if there have been enough failed attempts 
      #  (usually happens on larger arrays)
      #increase the size of the covariance matrix and try again
      if(running == 0):
        cov_size = min(mul_array(k_level), cov_size+1)
        running = 100
  
  return working_test

###############################################################
#End methods for randomized array generation
###############################################################

###############################################################
#Begin methods for greedy array generation
###############################################################

#Uses a greedy algorithm to make a covering array.
#Adds the first row that would give the most new interactions to the array, does this until the array is filled.
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
      #Check how many new interactions each row can provide
      for i in range(full.shape[0]):
        buckets[i] = buckets[i] + int( not (check == full[i,p]).all(1).any() )
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

###############################################################
#End methods for greedy array generation
###############################################################

###############################################################
#Begin methods for Hill Climbing array generation
###############################################################

#Recursively improve the CA by finding the rows that can be removed 
#  and removing them.
def hill_climbing(pre_hill, k_level, num_inter, step):
  #step is used to keep track of all the rows we have checked
  #Iterate through every row in the array
  for i in range(step, len(pre_hill)):
    #if it is found that a row can be removed...
    if(check_interactions(numpy.delete(pre_hill, i, 0), k_level, num_inter)):
      #print("We have to go deeper..." + str(i))
      #...recurse the program on itself with said row removed
      return hill_climbing(numpy.delete(pre_hill, i, 0), k_level, num_inter, i)
  return pre_hill

###############################################################
#End methods for Hill Climbing array generation
###############################################################

###############################################################
#Begin general methods for array generation
###############################################################

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
#General algorithm is to iteratively create all possible tuples up to the
#maximum value of the input array, then remove the ones that don't fit our
#established pattern.
def create_full_array(input_array):
  #Create an array in a format that can be passed to itertools
  give = []
  for i in input_array:
    give.append(list(numpy.arange(i)))
  
  #Pass said array to itertools
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
    mul = 1
    for i in p:
      mul = mul*k_level[i]
    #check if every possible interaction is represented
    if(numpy.unique(test[:,p], axis=0).shape[0] < mul):
      #if not, return false
      return False
  #if we made it through the whole for loop, return true
  return True

###############################################################
#End general methods for array generation
###############################################################

###############################################################
#Begin main
###############################################################

def main():
  #Start performance timer
  start = time.process_time()
  #get the number of interactions
  num_inter = int(sys.argv[1])
  #get the array
  k_level = sys.argv[2].split(',')
  k_level = numpy.asarray(sorted(list(map(int, k_level))))
  total = 1
  #Find the total number of combinations possible
  for i in k_level:
    total = total * i
  give = switch(k_level, num_inter)
  print(give)
  print(str(give.shape[1]) + " Elements in row.")
  print(str(give.shape[0]) + " Rows in covering array.")
  print(str(total) + " Rows possible.")
  end = time.process_time()
  print("Elapsed Time: " + str(end - start))

def switch(k_level, num_inter):
  check = int(sys.argv[3])
  full = create_full_array(k_level)
  give = []
  if(check == 1):
    #Randomized
    print("Randomized")
    give = create_cover(k_level, num_inter)
  elif(check == 2):
    #Greedy from Full
    print("Greedy from Full")
    give = greedy_generation(full, k_level, num_inter)
    #Sort the array, the greedy method returns an unsorted array
    for x in range(give.shape[1], 0, -1):
      give = give[numpy.argsort(give[:,x-1], kind='mergesort')]
  elif(check == 3):
    #Hill Climbing from Full
    print("Hill Climbing from Full")
    give = hill_climbing(full, k_level, num_inter, 0)
  elif(check == 4):
    #Greedy from Randomized
    print("Greedy from Randomized")
    give = greedy_generation(create_cover(k_level, num_inter), k_level, num_inter)
    #Sort the array, the greedy method returns an unsorted array
    for x in range(give.shape[1], 0, -1):
      give = give[numpy.argsort(give[:,x-1], kind='mergesort')]
  elif(check == 5):
    #Hill climbing from randomized
    print("Hill Climbing from Randomized")
    give = hill_climbing(create_cover(k_level, num_inter), k_level, num_inter, 0)
  else:
    print("Invalid input detected")
  return give

if __name__ == "__main__":
  main()


