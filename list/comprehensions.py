#  Basic: Square of numbers
nums = [1, 2, 3, 4, 5]
squares = [x**2 for x in nums]
print(squares)  # [1, 4, 9, 16, 25]


#  Filtering: Even numbers only
evens = [x for x in nums if x % 2 == 0]
print(evens)  # [2, 4]


#  Conditional expression inside comprehension
labels = ["even" if x % 2 == 0 else "odd" for x in nums]
print(labels)  # ['odd', 'even', 'odd', 'even', 'odd']


