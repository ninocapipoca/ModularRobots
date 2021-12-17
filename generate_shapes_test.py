# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 08:15:55 2021

@author: carol
"""

import to_bip as tb
import blocks as bl
import shapegen as sh
import randomgen as rand
import sys

def visual_print_2D(block):
    top = chr(9635) if block.top is not None else chr(9633)
    left = chr(9635) if block.left is not None else chr(9633)
    right = chr(9635) if block.right is not None else chr(9633)
    bot = chr(9635) if block.bot is not None else chr(9633)

    print(" Pos: ", block.name)
    print("      {}     ".format(top))
    print("     /    ")
    print("{} - {} - {}".format(left, chr(9640), right))
    print("     \     ")
    print("      {}     \n".format(bot))


def print_matrix(mat):
    for line in mat:
        print(str(line))

def main():

    print("Beginning block generation.. \n")

    print("---- Random 2D shape -----")
    rand2D = rand.random_shape2D(6)
    rand2D_blocks = bl.init_blocks_2D(rand2D.mat)
    rand2D_conn = bl.connect_blocks_2D(rand2D_blocks)
    print_matrix(rand2D.mat)
    print("\n")
    for block in rand2D_conn.values():
        print("\nBLOCK NAME: ", block.name)
        print("Left :", block.left.name if block.left is not None else "None")
        print("Right: ", block.right.name if block.right is not None else "None")
        print("Top :", block.top.name if block.top is not None else "None")
        print("Bottom :", block.bot.name if block.bot is not None else "None")
        print("---------------\n")

        visual_print_2D(block)

        print("---- Triangle ----")
        triangle = sh.Triangle(5)
        triangle.generate()
        triangle_blocks = bl.init_blocks_2D(triangle.mat)
        triangle_conn = bl.connect_blocks_2D(triangle_blocks)
        print_matrix(triangle.mat)
        print("\n")

        for block in triangle_conn.values():
            visual_print_2D(block)

    if args == 3:
        print("---- Sphere ----")
        sphere = sh.Sphere(5)
        sphere.generate()
        sphere_blocks = bl.init_blocks_3D(sphere.matlist())
        sphere_conn = bl.connect_blocks_3D(sphere_blocks)

        print("LAYERS:")
        for mat in sphere.matlist():
            print_matrix(mat)
            print("\n")
        print("\n")

        for block in sphere_conn.values():
            visual_print_2D(block)
            print("\n")

    if args == 4:
        print(" ---- Pyramid ----")
        py = sh.Pyramid(5)
        py.generate()
        py_blocks = bl.init_blocks_3D(py.matlist())
        py_conn = bl.connect_blocks_3D(py_blocks)

        for block in py_conn.values():
            visual_print_2D(block)
            print("\n")

        print("LAYERS:")
        for mat in py.matlist():
            print_matrix(mat)
            print("\n")
        print("\n")



if __name__ == "__main__":
    main()
