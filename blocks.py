# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 01:37:25 2021

@author: carol
"""

"""
Our connections dict is always of the following form -
dictstruct = {'left': ,  
              'right': ,
              'top': ,
              'bot': ,
              'front': ,
              'back': }
"""

class Block():
    # properties
    # connectors
    def __init__(self, connections = dict()):
        self.conns = connections
        
        
    
class Robot():
    def __init__(self, blocks):
        self.blocks = blocks


def init_blocks(mat):
    blocks = dict()
    for y in range(len(mat)):
        for x in range(len(mat)):
            if mat[y][x] == 1:
                blocks[(x,y)] = Block() # initialise w empty dictionary
    
    return blocks

def connect_right(line):
    # I have absolutely no idea why this doesn't work
    blocks = {}
    
    for i in range(len(line)):
        if line[i] == 1:
            blocks[i] = Block()
        
    for pos in blocks.keys():
        print("we are at pos", pos)
        if pos + 1 in blocks.keys():
            blocks[pos].conns['right'] = blocks[pos+1]
            
    return blocks
            
            
        
                
    
    
    