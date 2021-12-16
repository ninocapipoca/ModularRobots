#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from random import random, choice, randint
from itertools import product

dx = 1    # size of ambient space
res = .1  # resolution of the grid
x = np.arange(-dx, dx, res)
y = np.arange(-dx, dx, res)
z = np.arange(-dx, dx, res)
# grid
xx, yy, zz = np.meshgrid(x,y,z,sparse=True)


# primitives / nullary

def cuboid(x,y,z, xmin=-1, xmax=1, ymin=-1, ymax=1, zmin=-1, zmax=1):
    return (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax) & (z >= zmin) & (z <= zmax)

def cylinder(x,y,z, r=1, cx=0, cy=0, zmin=-1, zmax=1):
    return ((x-cx)**2 + (y-cy)**2 <= r*r) & (z >= zmin) & (z <= zmax)

def cone(x,y,z, r=1, cx=0, cy=0, zmin=-1, zmax=1):
    lin = (zmax-z) / (zmax-zmin) # linear interpolation
    return np.sqrt((x-cx)**2 + (y-cy)**2) <= lin * r

def pyramid(x,y,z, r=1, cx=0, cy=0, zmin=-1, zmax=1):
    lin = (zmax-z) / (zmax-zmin) # linear interpolation
    return np.maximum(np.abs(x-cx), np.abs(y-cy)) <= lin * r


# transform / unary

def translate(arr, dt):
    # trims what goes out
    out = np.roll(arr, dt)
    i,j,k = dt
    if i > 0: out[:i] = 0
    if i < 0: out[i:] = 0
    if j > 0: out[:,:j] = 0
    if j < 0: out[:,j:] = 0
    if k > 0: out[:,:,:k] = 0
    if k < 0: out[:,:,k:] = 0
    return out

def scale(arr, s):
    # scales from the center
    if s <= 1:
        out = arr * 0
        for coor in product(*map(range, arr.shape)):
            i,j,k = np.array(coor) // 4 + np.array(arr.shape) // 2
            out[i,j,k] |= arr[coor]
        return out
    assert isinstance(s, int)
    kernel = np.ones((s,s,s), dtype=bool)
    out = np.kron(arr, kernel)
    return out
    # if not resize: return out
    # # origin
    # i,j,k = (np.array(out.shape) - np.array(arr.shape)) // 2
    # out = out[i:,j:,k:]
    # # resize
    # i,j,k = arr.shape
    # return out[:i,:j,:k]

def rotate(arr, axis):
    # axis = +/- {1,2,3}
    i,j,k = arr.shape
    assert i==j==k
    times = 1 if axis > 0 else 3
    aa = np.abs(axis)
    axis = (aa-1, aa) if aa < 3 else (2,0)
    return np.rot90(arr, times, axis)


# compositions / binary

def union(a,b): return a | b
def intersect(a,b): return a & b
def diff(a,b): return a & ~b
def symm(a,b): return a ^ b

def show(arr):
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(arr)
    plt.show()

def random_gen(depth=1, p2=.5):
    """ p2 too big might cause infinite recursion """
    if random() < p2:
        fn = choice([union,intersect,diff,symm])
        print(">"*depth, fn)
        a,b = random_gen(depth+1),random_gen(depth+1)
        return fn(a,b)
    else:
        fn = choice([cuboid,cylinder,cone,pyramid])
        print(">"*depth, fn)
        arr = fn(xx,yy,zz)  # TODO better parameters
        if random() < 1:
            sc = random()
            print("-"*depth, "scale", sc)
            arr = scale(arr, sc)
        if random() < .2:
            i,j,k = np.array(arr.shape)-1
            dt = randint(-i,i),randint(-j,j),randint(-k,k)
            print("-"*depth, "translate", dt)
            arr = translate(arr, dt)
        if random() < .2:
            axis = randint(-3,3)
            print("-"*depth, "rotate", axis)
            arr = rotate(arr, axis)
        return arr


if __name__ == "__main__":
    arr = random_gen()
    show(arr)