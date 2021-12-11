### RANDOM SHAPE GENERATION ###

import shapegen as shp
import random as rand

def random_transform(shape):
    # transforms a shape by a random amount 
    x = rand.randint(-1*shape.d+1, shape.d-1)
    y = rand.randint(-1*shape.d+1, shape.d-1)
    return shape.transform(x,y)

def random_binmat(d):
    # generates a random binary matrix of dimension d x d
    return [[rand.randint(0,1) for x in range(d)] for y in range(d)]

def random_shape2D(d):
    # generates a completely random 2D shape
    # provided it fits in a matrix that is of dimension d x d
    generated = random_binmat(d)
    shape = shp.Shape2D(d, generated)
    while not shape.valid():
        generated = random_binmat(d)
        shape = shp.Shape2D(d, generated)
        
    return shape

def random_union(shape):
    # union with a random default shape
    pass

def generate_random(shapelist, max_size):
    pass
    

