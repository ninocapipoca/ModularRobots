# -*- coding: utf-8 -*-
import sys
sys.path.append("..") # Adds higher directory to python modules path.


import to_bip as tb
import blocks as bl
import shapegen as sh
import randomgen as rand



def main():

    print("Beginning block generation.. \n")

    print("---- Random 2D shape -----")
    rand2D = rand.random_shape2D(6)
    rand2D_blocks = bl.init_blocks_2D(rand2D.mat)
    rand2D_conn = bl.connect_blocks_2D(rand2D_blocks)
    bl.print_matrix(rand2D.mat)
    print("\n")
    for block in rand2D_conn.values():
        print("\nBLOCK NAME: ", block.name)
        print("Left :", block.left.name if block.left is not None else "None")
        print("Right: ", block.right.name if block.right is not None else "None")
        print("Top :", block.top.name if block.top is not None else "None")
        print("Bottom :", block.bot.name if block.bot is not None else "None")
        print("---------------\n")

        bl.visual_print_2D(block)

    tb.write_BIP("rand2D.bip", rand2D_conn)


if __name__ == "__main__":
    main()
