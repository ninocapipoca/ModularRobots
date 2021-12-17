# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 08:15:55 2021

@author: carol
"""

import to_bip as tb
import blocks as bl
import shapegen as sh
import randomgen as rand

def main():
    print("---- Random 2D shape -----")
    rand2D = rand.random_shape2D(6)
    rand2D_blocks = bl.init_blocks_2D(rand2D.mat)
    rand2D_conn = bl.connect_blocks_2D(rand2D_blocks)
    
    tb.write_bip("random_2d_shape.bip")

    
    

if __name__ == "__main__":
    main()