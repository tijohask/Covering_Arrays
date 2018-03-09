import sys
import numpy
import itertools
import time

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
def check_interactions(full, k_level, num_inter):
  cur = numpy.asarray([full[0,:]])
  full = numpy.delete(full, 0, 0)
  for x in range(full.shape[0]):
    buckets = [0]*full.shape[0]
    #get all existing combinations (interactions) from the data
    for p in itertools.combinations(numpy.arange(len(k_level)), num_inter):
      #If check contains the interaction, then buckets will not increment
      check = numpy.unique(cur[:,p], axis=0)
      for i in range(full.shape[0]):
        buckets[i] = buckets[i] + int( not (check == full[i,p]).all(1).any() )
        #print(not (check == full[i,p]).all(1).any())
    if(max(buckets) == 0):
      return cur
    idx = buckets.index(max(buckets))
    cur = numpy.append(cur, [full[idx]], axis=0)
    full = numpy.delete(full, buckets.index(max(buckets)), 0)

start = time.process_time()
#Take the system arguments
#get the desired number of interactions
num_inter = int(sys.argv[1])

#get the array
k_level = sys.argv[2]
k_level = k_level.split(',')
k_level = numpy.asarray(sorted(list(map(int, k_level))))

full = create_full_array(k_level)

greedy_array = check_interactions(full, k_level, num_inter)
print(greedy_array)
print(greedy_array.shape)
print(full.shape)
end = time.process_time()
print("Elapsed Time: " + str(end - start))


