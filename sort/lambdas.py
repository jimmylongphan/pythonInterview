nums = [5, 2, 9, 1, 5, 6]

#####################################################################################
# INTEGERS
# Sort ascending
nums.sort()
print(nums)  # [1, 2, 5, 5, 6, 9]

# Sort descending using lambda (just for demo; you can also use reverse=True)
nums.sort(key=lambda x: -x)
print(nums)  # [9, 6, 5, 5, 2, 1]
#####################################################################################
# TUPLES
data = [("apple", 5), ("banana", 2), ("cherry", 7), ("date", 3)]

# Sort by second element descending, then first element ascending
data.sort(key=lambda x: (-x[1], x[0]))

# Sort by second int descending, then first string descending
# This reverses the string characters for sorting, so 'apple' becomes 'elppa', 
# which when sorted ascending effectively reverses the original order.
data.sort(key=lambda x: (-x[1], x[0][::-1]))

# Sort by first element (string) ascending
data.sort(key=lambda x: x[0])
print(data)  # [('apple', 5), ('banana', 2), ('cherry', 7), ('date', 3)]

# Sort by second element (integer) descending
data.sort(key=lambda x: x[1], reverse=True)
print(data)  # [('cherry', 7), ('apple', 5), ('date', 3), ('banana', 2)]

# Sort by length of first element string
data.sort(key=lambda x: len(x[0]))
print(data)  # [('date', 3), ('apple', 5), ('banana', 2), ('cherry', 7)]


#####################################################################################
# CLASS

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"Person({self.name}, {self.age})"

people = [
    Person("Alice", 30),
    Person("Bob", 25),
    Person("Charlie", 35),
    Person("David", 25)
]

# Sort by age ascending
people.sort(key=lambda p: p.age)
print(people)
# [Person(Bob, 25), Person(David, 25), Person(Alice, 30), Person(Charlie, 35)]

# Sort by age ascending, then by name ascending
people.sort(key=lambda p: (p.age, p.name))
print(people)
# [Person(Bob, 25), Person(David, 25), Person(Alice, 30), Person(Charlie, 35)]

# Sort by name descending
people.sort(key=lambda p: p.name, reverse=True)
print(people)
# [Person(David, 25), Person(Charlie, 35), Person(Bob, 25), Person(Alice, 30)]
