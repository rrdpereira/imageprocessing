import numpy as np

# A = np.diag([1,3,5,7]).reshape(16,)
# A_flipped =np.fliplr(A)
# print(A_flipped)

A = np.diag([1,3,5,7,8]).reshape(5,5)
A_flipped =np.fliplr(A)
print(A_flipped)

xs = [[3, 1, 4], [1, 5, 9]]
res = np.fliplr(xs)
print(res)

xs = [[3], [1], [4]]
res = np.fliplr(xs)
print(res)