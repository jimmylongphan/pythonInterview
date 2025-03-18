"""
Given an m x n integer matrix heightMap representing the height of each unit cell in a 2D elevation map, return if one location can trap water. Cell at coordinates (row, col) in the matrix can trap water if there's a boundary around it have greater heights


input: matrix, row, col
output True/False


water can only flow in 4 directions and no water can be trap on edge
    - no water on edge / boundary
Example 1:


algorithm:
    for a target cell, check all neighbors
        - cannot be boundary
        - must have higher height
        if they have lower height
            - call recursive or dfs on lower cell
            - need a visited array
    if hit a boundary
        boundary must have higher height otherwise leak


height:
[[3,3,3,3,3],
 [3,2,2,2,3],
 [3,2,1,2,3],
 [3,2,2,2,3],
 [3,3,3,3,3]]
 
input: (2, 2)
output: True


Example 2:


height:
[[1,4,3,1,3,2],
 [3,2,1,3,2,4],
 [2,3,3,2,3,1]]


input: (1, 4) Is the value 2?
output: True, all the neighbors are higher than this location


input: (1, 1) value 2 -> also check right neighbor 1
    (1,1) is already visited
    (1,2) return True
    for cell (1,1) all neighbors higher and lower neighbors can trap water
output: True, because there's boundary surrounding (1, 1) and (1, 2)


input: (0, 0)
output: False, it's on edge


Example 3:


height:
[[2,2,2,2,1,2],
 [2,1,2,1,1,2],
 [2,1,0,0,2,2],
 [2,2,2,2,2,2]]


input: (2, 2) 0 -> neighbor 0 has higher neighbors
output: True, 1 unit of water can be trapped in (2, 2)


input: (1, 1)
    value 1 has 3 higher neighbrs
    value 1 at (2, 1) has one lower neighbor
    value 0 at (2, 2) has 2 higher and 1 lower
    value 0 at (2, 3) has 2 higher neighbors but 1 boundary at
output: False, water can leak via (0, 4)
"""

directions = [[0,1], [0,-1], [1,0], [-1,0]]

def trap_water(matrix: list[list[int]], target: list[int]) -> bool:
    rows = len(matrix)
    cols = len(matrix[0])

    current_row = target[0]
    current_col = target[1]

    # create visited
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # call dfs on the target
    result = dfs(matrix, current_row, current_col, matrix[current_row][current_col], visited)

    return result


"""
algorithm:
    for a target cell, check all neighbors
        - cannot be boundary
        - must have higher height
        if they have lower height
            - call recursive or dfs on lower cell
            - need a visited array
    if hit a boundary
        boundary must have higher height otherwise leak
"""


def dfs(matrix: list[list[int]], current_row: int, current_col: int, original_height: int, visited: list[list[bool]]) -> bool:
    rows = len(matrix)
    cols = len(matrix[0])

    # dont repeat
    if visited[current_row][current_col]:
        return True
    
    # mark as visited
    visited[current_row][current_col] = True

    # compare boundary
    if current_row == 0 or current_col == 0 or current_row == rows-1 or current_col == cols - 1:
        if matrix[current_row][current_col] <= original_height:
            # leaks here
            return False

    # not at boundary
    # if neighbor has greater height, then good
    if matrix[current_row][current_col] > original_height:
        return True

    # go through neighbors
    for r_add, c_add in directions:
        r2 = current_row + r_add
        c2 = current_col + c_add

        # check out of bounds
        if r2 < 0 or r2 >= rows or c2 < 0 or c2 >= cols:
            continue

        dfs_result = dfs(matrix, r2, c2, original_height, visited)
        if not dfs_result:
            return False

    # did not find any leaks
    return True


input = [[2,2,2,2,1,2],
 [2,1,2,1,1,2],
 [2,1,0,0,2,2],
 [2,2,2,2,2,2]]

# input: (2, 2)
# output: True

result = trap_water(input, [2,2])
print(f"result is {result}")

input = [
 [1,4,3,1,3,2],
 [3,2,1,3,2,4],
 [2,3,3,2,3,1]]


#input: (1, 4) Is the value 2?
# output: True, all the neighbors are higher than this location
result = trap_water(input, [1,4])
print(f"result is {result}")

input = [[3,3,3,3,3],
 [3,2,2,2,3],
 [3,2,1,2,3],
 [3,2,2,2,3],
 [3,3,3,3,3]]


#input: (2, 2)
#output: True

result = trap_water(input, [2, 2])
print(f"result is {result}")

input = [[1,4,3,1,3,2],
 [3,2,1,3,2,4],
 [2,3,3,2,3,1]]


# input: (1, 4) Is the value 2?
# output: True, all the neighbors are higher than this location
result = trap_water(input, [1,4 ])
print(f"result is {result}")


#input: (1, 1) value 2 -> also check right neighbor 1
#output: True, because there's boundary surrounding (1, 1) and (1, 2)
result = trap_water(input, [1,1 ])
print(f"result is {result}")

#input: (0, 0)
#output: False, it's on edge
result = trap_water(input, [0,0])
print(f"result is {result}")

input = [
 [2,2,2,2,1,2],
 [2,1,2,1,1,2],
 [2,1,0,0,2,2],
 [2,2,2,2,2,2]]

#input: (2, 2) 0 -> neighbor 0 has higher neighbors
#output: True, 1 unit of water can be trapped in (2, 2)
result = trap_water(input, [2,2])
print(f"result is {result}")

# dfs should be called for [2,1], [2, 2], [2, 3], [1, 3], [1,4], [0,4] 

# input: (1, 1)
# output: False, water can leak via (0, 4)
result = trap_water(input, [1,1])
print(f"result is {result}")

