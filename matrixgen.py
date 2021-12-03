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


def generate_circle(r, width, height, a, b):
    mat = [['0' for x in range(width)] for y in range(height)]

    # draw the circle
    for y in range(height):
        for x in range(width):
            dist = abs((x-a)**2 + (y-b)**2)
            if dist <= r**2:
            #if math.sqrt(x**2 + y**2) > d:
                mat[y][x] = '1'

    return mat




#print(DataFrame(map_))

width, height = 5, 5
a, b = height//2, height//2
r = a

mat = generate_circle(r, width, height, a, b)
#print the map
for line in mat:
    print(' '.join(line))
