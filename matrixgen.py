from pandas import *
import math
# def generate_circle(d):
#     mat = [[1 for i in range(d)] for j in range(d)]
#     remove = (d-3)//2
#     cnt = 0
#     for i in range(remove):
#         for j in range(d):
#             if j < remove or j > remove+2:
#                 mat[i][j] = 0
#
#     for i in range(remove+3, d):
#         mat[i] = mat[i-(d-remove)]
#
#
#     return mat

# def generate_circle(d, a, b, eps):
#     mat = [[0 for x in range(d)] for y in range(d)]
#
#     for y in range(d):
#         for x in range(d):
#             if abs((x-a)**2 + (y-b)**2 - (d//2)**2) < eps**2:
#                 mat[y][x] = 0
#
#
# mat = generate_circle(7, 5, 5, 2.2)
# print(DataFrame(mat))

# def generate_circle(r, d, a, b):
def generate_circle(d):
    r = d//2
    a = d//2
    mat = [[0 for x in range(d)] for y in range(d)]

    # draw the circle
    for y in range(d):
        for x in range(d):
            dist = abs((x-a)**2 + (y-a)**2)
            if dist <= r**2:
                mat[y][x] = 1

    return mat


def prettyprint_mat(mat):
    for y in range(len(mat)):
        for x in range(len(mat)):
            mat[y][x] = str(mat[y][x])

    for line in mat:
        print(' '.join(line))

# TESTING
mat = generate_circle(7)
prettyprint_mat(mat)

# FOR TESTING PURPOSES but no longer in use
#print(DataFrame(map_))

# mat = generate_circle(7)
# #print the map
# for line in mat:
#     print(' '.join(line))
