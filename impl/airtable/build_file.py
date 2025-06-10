from collections import defaultdict
from collections import deque

"""
Similar to course schedule
"""

class Solution():
    rules = []
    dependencyCount = defaultdict(int)
    dependents = defaultdict(list)
    fileDependencies = defaultdict(list)
    completedFiles = set()

    def __init__(self, rules: list):
        self.rules = rules
        self.initializeDependencies()

    def initializeDependencies(self) -> None:
        for rule_map in self.rules:
            for parent, children in rule_map.items():
                self.fileDependencies[parent] = children
                self.dependencyCount[parent] = len(children)
                for child in children:
                    self.dependents[child].append(parent)

    """
    Goes through all the dependencies of the target
    And for any file that does not have dependency, it can start
    """
    def startBuild(self, target: str) -> list:
        ready_to_build = set()
        queue = deque()
        visited = set()

        queue.append(target)
        visited.add(target)

        while queue:
            current = queue.popleft()
            print(f"current is {current}")

            if current in self.fileDependencies:
                for child in self.fileDependencies[current]:
                    print(f"child is {child}")
                    if self.dependencyCount[child] == 0 and child not in self.completedFiles:
                        ready_to_build.add(child)

                    if child not in visited:
                        queue.append(child)
                        visited.add(child)

        return ready_to_build
    
    """
    Set the target file to completed
    Then find other files tht are ready to be built
    because they do not have dependencies
    """
    def onComplete(self, target: str) -> list:
        self.completedFiles.add(target)
        next_to_build = []

        if target in self.dependents:
            for dependent in self.dependents[target]:
                self.dependencyCount[dependent] -= 1
                if self.dependencyCount[dependent] == 0 and dependent not in self.completedFiles:
                    next_to_build.append(dependent)

        return next_to_build



# list of maps
rules = []
rules.append({
    "parent1": ["child1", "child2"]
})
rules.append({
    "parent2": ["child3", "child4"]
})
rules.append({
    "parent3": ["parent1", "parent2"]
})
rules.append({
    "parent4": ["child5", "child6"]
})

solution = Solution(rules=rules)

result = solution.startBuild("parent1") # output [child1, child2]
print(f"result = {result}")

result = solution.onComplete("child1") # Output: []
print(f"result = {result}")

result = solution.onComplete("child2") # Output: [parent1]
print(f"result = {result}")

# Run Standalone Output: [child1, child2, child3, child4]
# But when child1 and child1 are on completed, then result is {'parent1', 'child4', 'child3'}
result = solution.startBuild("parent3") 
print(f"result = {result}")

result = solution.startBuild("parent4") #  Output: [child5, child6]
print(f"result = {result}")
