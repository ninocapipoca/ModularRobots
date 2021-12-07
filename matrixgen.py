from pandas import *
import math

    
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

def generate_triangle(d):
    """generates a triangle of base length d"""
    # note that if d is an even number, the top of the triangle
    # will be made up of 2 blocks
    
    mat =[]
    cnt = d
    zcnt = 0
    for i in range(d):
        addme = [1 for x in range(cnt)]
        withzeroes = add_zeroes(addme, zcnt//2)

        if len(withzeroes) > d:
            mat.append([0 for x in range(d)])
        else:
            mat.append(withzeroes)
            
        cnt -= 2
        zcnt += 2
        
    return mat[::-1] # return the reverse of the matrix


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
