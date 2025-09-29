
"""
// We have a set of drones that are positioned over an area they are tasked with
// searching. Each of the drones has a mounted camera that can view a section of
// the area below.
//
// Each drone's viewable section of the search area can be
// defined as a circle centered at some (x, y) point on the ground.
// Example viewable area: {x, y, radius} (type: vector<int>, size: 3)
//
// On the ground, there are several targets that need to be looked at by the
// drones' mounted cameras. Each target can be defined as an (x, y) point.
// Example target: {x, y} (type: vector<int>, size: 2)
//
// Given a vector of viewable areas and a vector of ground targets, write a
// function or set of functions to determine how many targets are viewable by
// each drone's camera.
//
//
// Example 1:
//
// targets: {{1,3},{3,3},{5,3},{2,2}}
// viewable areas: {{2,3,1},{4,3,1},{1,1,2}}
//
// viewable target counts: {3, 2, 2}
//    2,3,1 -> can see 3  {1,3}, {3,3}, {2,2}
//    4,3,1 -> can see 2 {3,3}, {5,3}
//    1,1,2 -> can see 2 {1,3}, {2,2}   {3,3}?
//
// Example 2:
//
// targets: {{1,1},{2,2},{3,3},{4,4},{5,5}}
// viewable areas: {{1,2,2},{2,2,2},{4,3,2},{4,3,3}}
//
// viewable target counts: {2, 3, 2, 4}

OPTIMAL SOLUTION
  - for each circle create the range of x and y
  - sort the input targets 
    - binary search on the input targets x and y
    - don't need to check points outside of range

trick:
  sort and sweep
"""
import math



def get_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    side_a = abs(x1 - x2)
    side_b = abs(y1 - y2)
    c_square = side_a * side_a + side_b * side_b
    c = math.sqrt(c_square)
    return c
    
def count_viewable_areas(targets, viewable_areas) -> list[int]:
    result = []
    
    for va in viewable_areas:
        current_count = 0
        for target in targets:
            radius = va[2]
            
            distance = get_distance(va[0], va[1], target[0], target[1])
            if distance <= radius:
                current_count += 1
        result.append(current_count)
    
    return result
    

targets_1 = [[1,3],[3,3],[5,3],[2,2]]
viewable_areas_1 = [[2,3,1],[4,3,1],[1,1,2]]

results_1 = count_viewable_areas(targets=targets_1, viewable_areas=viewable_areas_1)
print(f"results example 1: {results_1}")


targets_2 = [[1,1],[2,2],[3,3],[4,4],[5,5]]
viewable_areas_2 = [[1,2,2],[2,2,2],[4,3,2],[4,3,3]]
results_2 = count_viewable_areas(targets=targets_2, viewable_areas=viewable_areas_2)
print(f"results example 2: {results_2}")


# all outside of range
targets_3 = [[1,1],[2,2],[3,3],[4,4],[5,5]]
viewable_areas_3 = [[1,2,0],[2,2,0],[4,3,0],[4,3,0]]
results_3 = count_viewable_areas(targets=targets_3, viewable_areas=viewable_areas_3)
print(f"results example all outside range: {results_3}")


# all inside range
targets_4 = [[1,1],[2,2],[3,3],[4,4],[5,5]]
viewable_areas_4 = [[1,2,100],[2,2,100],[4,3,100],[4,3,100]]
results_4 = count_viewable_areas(targets=targets_4, viewable_areas=viewable_areas_4)
print(f"results example all inside range: {results_4}")



# negative numbers
targets_5 = [[-1,-1]]
viewable_areas_5 = [[-1,-2,100]]
results_5 = count_viewable_areas(targets=targets_5, viewable_areas=viewable_areas_5)
print(f"results negative: {results_5}")
