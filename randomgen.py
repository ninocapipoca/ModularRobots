### RANDOM SHAPE GENERATION ###

import shapegen as shp
import random as rand

# NOTE - the function that checks whether an arrangement is valid
# doesn't work properly - must be fixed in shapegen.py

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

def random_union(shape, maxsize):
    # This function doesn't work properly, an attempt was made but it was
    # unsuccessful :(
    
    # union with a random shape of max dimension maxsize
    # returns the matrix of shape when union has been performed
    d = rand.randint(1, maxsize)
    
    randshape = {1 : shp.Circle(d), 
                 2 : shp.Square(d), 
                 3 : shp.Triangle(d),
                 4 : random_shape2D(d)}
    if d%2 != 1: # if d is even we can't draw a circle
        i = rand.randint(2,4)
    else: 
        i = rand.randint(1,4)
        
    ushape = randshape[i]
    print("random shape is", ushape)
    
    mat = ushape.generate()
    print("random shape matrix is", ushape.mat)
    
    return shape.union(ushape)
    

def generate_random(shapelist, max_size):
    pass
    

