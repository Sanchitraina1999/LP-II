# -*- coding: utf-8 -*-
"""Assignment-OR.ipynb

- **Transportation problems** deal with the movement of commodities from different sources to different destinations, with the overall objective of minimizing transportation costs

Prerequisites
- n = The number of sources.
- m = The number of destinations.
- supply = The total quantity available at each source.
- demand = The total quantity required at each destination.
- cost_mat = The cost of transportation of one unit of the commodity from each source to each destination.

## **INPUT**
"""

n = int(input("Number of supply centers : "))  
supply = list(map(int,input("Availablity at each centers: ").strip().split()))[:n]
# supply = [150,160,90]
print(supply)

m = int(input("\nNumber of destination centers : "))  
demand = list(map(int,input("Demand at each centers: ").strip().split()))[:m]
# demand = [140, 120, 90, 50]
print(demand)

import numpy as np 
print("\nEnter the cost matrix : ")
cost_mat = np.array(list(map(int, input().split())) ).reshape(n, m) 
# cost_mat = 16 18 21 12 17 19 14 13 32 11 15 10
print(cost_mat)

print( "Balanced Transportation problem" if sum(supply) == sum(demand) else "Unbalanced Transportation problem" )

"""## **North West Corner Method**

- Select North-West Corner cell



"""

print(supply)
print(demand)
print(cost_mat)

def north_west_corner(supply,demand):
  
  supply_c = supply.copy()
  demand_c = demand.copy()
  
  i,j = 0,0
  mat = []
  
  while len(mat) < len(supply) + len(demand) - 1 : # n + m - 1 constraints
  
    s = supply_c[i]
    d = demand_c[j]
    value = min(s,d)
  
    supply_c[i] -= value
    demand_c[j] -= value
    mat.append([(i,j),value])
  
    if supply_c[i] == 0 and i < len(supply)-1:
      i+=1
    if demand_c[j] == 0 and j < len(demand)-1:
      j+=1
  
  return mat

mat = north_west_corner(supply,demand)
print(mat)

cost = 0
for i in range(len(mat)):
  cost += ( cost_mat[ mat[i][0][0] ][ mat[i][0][1] ] * mat[i][1] )
print(cost)

"""## **Least Cost Method**

- Select the least value among all the costs
"""

print(supply)
print(demand)
print(cost_mat)

#Helper function which returns the minimum value alongwith its index

def get_min(c):

  i_min,j_min = 0,0
  minimum = 10**18 
  maxx = 10**18

  for i in range(n):
    for j in range(m):
      if c[i][j] < minimum and c[i][j] is not maxx :
        i_min, j_min, minimum = i, j, c[i][j]      
      
  return [i_min,j_min,minimum]

def least_cost(supply,demand,cost_mat):

  mat = []
  supply_c = supply.copy()
  demand_c = demand.copy()
  cost_mat_c = cost_mat.copy()

  i,j= 0,0
  maxx = 10**18

  while len(mat) < len(supply) + len(demand) - 1 : 
    
    result = get_min(cost_mat_c) # Get the index of minimum value in the cost matrix
    
    i = result[0]
    j = result[1]
    cost = result[2]
    s = supply_c[i]
    d = demand_c[j]
    value = min(s,d)

    supply_c[i] -= value
    demand_c[j] -= value

    mat.append([(i,j), value, cost ])
      
    if supply_c[i] == 0:    #Mark that row
      for k in range(m):
        cost_mat_c[i][k] = maxx

    if demand_c[j] == 0:  #Mark that column
      for k in range(n):
        cost_mat_c[k][j] = maxx
  return mat

mat = least_cost(supply,demand,cost_mat)
print(mat)

cost = 0
for i in range(len(mat)):
    cost += ( mat[i][1] * mat[i][2] ) 
print(cost)

"""## **Vogel’s Approximation Method**

- Find in the differences between the two lowest costs in each row and column. These are known as penalties/ extra costs.
- Find the maximum value among the penalties
- Look into the respective row or column accordingly and select the least value among all the costs
"""

print(supply)
print(demand)
print(cost_mat)

def calculate_row_penalty(c):
  maxx = 10**18
  r_penalty = []
  for i in range(n):
    # first, second = maxx, maxx
    a = []
    for j in range(m):
    	a.append(c[i][j])	
    a.sort()	
    first, second = maxx, maxx
    if a[0]==first:
    	first=0
    else:
    	first=a[0]	
    if a[1]==second:
    	second=0
    else:
    	second=a[1]
    r_penalty.append(abs(second-first))		
      # if c[i][j] < first and c[i][j] != maxx:
      #   second = first
      #   first = c[i][j]
      # elif ( c[i][j] < second and c[i][j] != first and c[i][j] != maxx  ):
      #   second = c[i][j]

    # if second == first and first == maxx : 
    #   r_penalty.append(-maxx)
    # else:
    #   r_penalty.append(second-first)

  return r_penalty

def calculate_col_penalty(c):
  maxx = 10**18
  c_penalty = []

  for j in range(m):
    # first, second = maxx, maxx
    a = []
    for i in range(n):
    	a.append(c[i][j])	
    a.sort()	
    # print(a)
    first, second = maxx, maxx
    if a[0]==first:
    	first=0	
    else:
    	first=a[0]	
    if a[1]==second:
    	second=0
    else:
    	second=a[1]
    c_penalty.append(abs(second-first))		

  # for j in range(m):
  #   first, second = maxx, maxx
  #   for i in range(n):
  #     if c[i][j] < first and c[i][j] != maxx:
  #       second = first
  #       first = c[i][j]
  #     elif ( c[i][j] < second and c[i][j] != first and c[i][j] != maxx ):
  #       second = c[i][j]

  #   if second == first and first == maxx : 
  #     c_penalty.append(-maxx)
  #   else:     
  #     c_penalty.append(second-first)

  return c_penalty

def vogels_approx(supply,demand,cost_mat):
  
  supply_c = supply.copy()
  demand_c = demand.copy()
  cost_mat_c = cost_mat.copy()

  row_penalty = []
  col_penalty = []
  mat = []
  
  maxx = 10**18

  while len(mat) < len(supply) + len(demand) - 1 :
    
    row_penalty = calculate_row_penalty(cost_mat_c)
    col_penalty = calculate_col_penalty(cost_mat_c)

    row_max = max(row_penalty)
    col_max = max(col_penalty)    
    
    i_index, j_index = 0, 0
    s,d,value = [],[],0

    if col_max > row_max:

      #Get the column index
      col_index = col_penalty.index(col_max)    
      minimum = 10**18

      #Select minimum from the column
      for i in range(n):
        if cost_mat_c[i][col_index] < minimum:
          minimum = cost_mat_c[i][col_index]
          i_index = i 
          j_index = col_index

    else:

      #Get the row index
      row_index = row_penalty.index(row_max)
      minimum = 10**18

      #Select minimum from the row
      for j in range(m):
        if cost_mat_c[row_index][j] < minimum :
          minimum = cost_mat_c[row_index][j]
          i_index = row_index
          j_index = j

    #Check respective supply and demand at index of minimum value
    s = supply_c[i_index]
    d = demand_c[j_index]      
      
    value = min(s,d)
    supply_c[i_index] -= value
    demand_c[j_index] -= value 
    
    mat.append([(i_index,j_index),value])

    # If supply is 0 cross out the particular row
    if supply_c[i_index] == 0 :
      for j in range(m):
        cost_mat_c[i_index][j] = maxx
        
    # Else if demand is 0 cross out the particular column
    elif demand_c[j_index] == 0 :  
      for i in range(n):  
        cost_mat_c[i][j_index] = maxx 

  return mat

mat = vogels_approx(supply,demand,cost_mat)
print(mat)

cost = 0
for i in range(len(mat)):
  cost += ( cost_mat[ mat[i][0][0] ][ mat[i][0][1] ] * mat[i][1] )
print(cost)
