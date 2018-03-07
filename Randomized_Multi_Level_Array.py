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

def create_full_array(input_array):
  arr = []
  arr_add = True
  for i in itertools.product(numpy.arange(max(input_array)), repeat=len(input_array)):
    arr_add = True
    for x in range(len(input_array)):
      if(input_array[x] <= i[x]):
        arr_add = False
        break
    if(arr_add):
      arr.append(list(i))
  return numpy.asarray(arr)


num_inter = int(sys.argv[1])

k_level = sys.argv[2]
k_level = k_level.split(',')
k_level = sorted(list(map(int, k_level)))
print(k_level)
print("Max Level: " + str(max(k_level)))
print("Length of array: " + str(len(k_level)))
print(create_full_array(k_level))








