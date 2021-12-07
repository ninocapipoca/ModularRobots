# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:33:32 2021

@author: carol
"""

# OLD CODE THAT DOES NOT WORK, for the report if necessary


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