import numpy as np

test = [
    [1, [0, 1]],
    [-1, [0, 1]],
    [0, [1, 0]],
    [1, [0, 1]]
]

values = [1, 2, 3, 4, 5]

print(np.argmax(test, 0))
# index = 0
# indexes = []
# for x in test:
#     if x == [0, 1]:
#         indexes.append(index)
#     index += 1
# print(indexes)
# print()
