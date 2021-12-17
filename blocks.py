# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 01:37:25 2021

@author: carol
"""

import shapegen as shp

class Block():
    # properties
    # connectors
    def __init__(self, name, power=False,
                 left=None, right=None, back=None, front=None, top=None, bot=None):
        self.left = left
        self.right = right
        self.front = front
        self.top = top
        self.bot = bot
        self.name = name
        self.power = power

        if self.power:
            self.back = None
        else:
            self.back = back

    def __str__(self):
        return "block name: " + self.name

    def BIP_instance(self):
        if self.power:
            blocktype = "Cube_BlinkyBlock_With_Cable_Port"
        else:
            blocktype = "CubeBlinkyBlock"
        blinkyStr = "\t\tcomponent BlinkyBlock.{} BlinkyBlock{}({})".format(blocktype, self.name, self.name)

        return blinkyStr

    def BIP_connect_bottom(self): # connects the bottom side of self with the top of self.bottom
        if self.bot is None:
            return ""

        connectstr = "\t\tconnector Synchron2_int connect_b{}_t{}(BlinkyBlock{}.CONNECT_BOTTOM, BlinkyBlock{}.CONNECT_TOP)".format(
            self.name, self.bot.name, self.name, self.bot.name)

        disconstr = "\t\tconnector Synchron2_int disconnect_b{}_t{}(BlinkyBlock{}.DISCONNECT_BOTTOM, BlinkyBlock{}.DISCONNECT_TOP)".format(
            self.name, self.bot.name, self.name, self.bot.name)
        return connectstr + "\n" + disconstr

    def BIP_connect_top(self): # connects the top side of self with the bottom of self.top
        if self.top is None:
            return ""

        connectstr = "\t\tconnector Synchron2_int connect_b{}_t{}(BlinkyBlock{}.CONNECT_BOTTOM, BlinkyBlock{}.CONNECT_TOP)".format(
            self.top.name, self.name, self.top.name, self.name)

        disconstr = "\t\tconnector Synchron2_int disconnect_b{}_t{}(BlinkyBlock{}.DISCONNECT_BOTTOM, BlinkyBlock{}.DISCONNECT_TOP)".format(
            self.top.name, self.name, self.top.name, self.name)
        return connectstr + "\n" + disconstr

    def BIP_connect_left(self):# connects the right side of self with the left of self.right
        if self.right is None:
            return ""
        else:
            connectstr = "\t\tconnector Synchron2_int connect_r{}_l{}(BlinkyBlock{}.CONNECT_RIGHT, BlinkyBlock{}.CONNECT_LEFT)".format(
                self.name, self.right.name, self.name, self.right.name)

            disconstr = "\t\tconnector Synchron2_int disconnect_r{}_l{}(BlinkyBlock{}.DISCONNECT_RIGHT, BlinkyBlock{}.DISCONNECT_LEFT)".format(
                self.name, self.right.name, self.name, self.right.name)
            return connectstr + "\n" + disconstr

    def BIP_connect_right(self): # connects the left side of self with the right side of self.left
        if self.left is None:
            return ""

        connectstr = "\t\tconnector Synchron2_int connect_l{}_r{}(BlinkyBlock{}.CONNECT_RIGHT, BlinkyBlock{}.CONNECT_LEFT)".format(
            self.left.name, self.name, self.left.name, self.name)

        disconstr = "\t\tconnector Synchron2_int disconnect_l{}_r{}(BlinkyBlock{}.DISCONNECT_RIGHT, BlinkyBlock{}.DISCONNECT_LEFT)".format(
            self.left.name, self.name, self.left.name, self.name)
        return connectstr + "\n" + disconstr

    def BIP_connect_front(self): # connects the front of self with the back of self.front
        if self.front is None:
            return ""

        connectstr = "\t\tconnector Synchron2_int connect_f{}_b{}(BlinkyBlock{}.CONNECT_FRONT, BlinkyBlock{}.CONNECT_BACK)".format(
            self.name, self.front.name, self.name, self.front.name)

        disconstr = "\t\tconnector Synchron2_int disconnect_f{}_b{}(BlinkyBlock{}.DISCONNECT_FRONT, BlinkyBlock{}.DISCONNECT_BACK)".format(
            self.name, self.front.name, self.name, self.front.name)
        return connectstr + "\n" + disconstr

    def BIP_connect_back(self): # connects the back of self with the front of self.back
        if self.back is None:
            return ""

        connectstr = "\t\tconnector Synchron2_int connect_b{}_f{}(BlinkyBlock{}.CONNECT_FRONT, BlinkyBlock{}.CONNECT_BACK)".format(
            self.back.name, self.name, self.back.name, self.name)

        disconstr = "\t\tconnector Synchron2_int disconnect_b{}_f{}(BlinkyBlock{}.DISCONNECT_FRONT, BlinkyBlock{}.DISCONNECT_BACK)".format(
            self.back.name, self.name, self.back.name, self.name)
        return connectstr + "\n" + disconstr


def init_blocks_2D(mat):
    # only useful for 2D shapes
    # initializes blocks for a 2D matrix
    blocks = dict()
    for y in range(len(mat)):
        for x in range(len(mat)):
            if mat[y][x] == 1:
                blocks[(y,x)] = Block("{},{}".format(y,x)) # initialise w no connections

    return blocks


def connect_blocks_2D(blocks):
    # this is only useful for 2D shapes
    # was used as a something to build on for definining the same function
    # for 3D shapes

    # connects blocks left, right, top and bottom for a 2D matrix
    for pos in blocks.keys():
        row, col = pos

        if (row + 1, col) in blocks.keys(): # connect bottom
            conn = blocks[(row+1, col)]
            blocks[(row, col)].bot = conn

        if (row - 1, col) in blocks.keys(): # connect top
            conn = blocks[(row-1, col)]
            blocks[(row, col)].top = conn

        if (row, col + 1) in blocks.keys(): # connect right
            conn = blocks[(row, col+1)]
            blocks[(row, col)].right = conn

        if (row, col - 1) in blocks.keys(): # connect left
            conn = blocks[(row, col-1)]
            blocks[(row, col)].left = conn

    return blocks

def mergedicts(dict1, dict2):
    # unused auxiliary function
    # merges dictionary 2 into dictionary 1
    for key in dict2.keys():
        if key in dict1:
            print("There already exists an entry {} with key {}".format(dict1[key], key))
            print("Error - please make sure that each key is unique")
            return

        else:
            dict1[key] = dict2[key]

# 3D SHAPES ARE DEFINED FROM BOTTOM TO TOP
class Robot():
    def __init__(self, blocks):
        assert isinstance(blocks, dict)
        self.blocks = blocks


def init_blocks_3D(matlist):
    # initialises the blocks for a 3D matrix
    blocks = dict()
    for z in range(len(matlist)):
        mat = matlist[z]
        for y in range(len(mat)):
            for x in range(len(mat[0])):

                if mat[y][x] == 1:
                    blocks[(z,y,x)] = Block("{},{},{}".format(z,y,x))

    return blocks


def connect_blocks_3D(blocks):
    for pos in blocks.keys():
        layer, row, col = pos

        if (layer-1, row, col) in blocks.keys(): # connect bottom
            conn = blocks[(layer-1, row, col)]
            blocks[(layer, row, col)].bot = conn

        if (layer+1, row, col) in blocks.keys(): # connect top
            conn = blocks[(layer+1, row, col)]
            blocks[(layer, row, col)].top = conn

        if (layer, row-1, col) in blocks.keys(): # connect back
            conn = blocks[(layer, row-1, col)]
            blocks[(layer, row, col)].front = conn

        if (layer, row+1, col) in blocks.keys(): # connect front
            conn = blocks[(layer, row+1, col)]
            blocks[(layer, row, col)].front = conn

        if (layer, row, col-1) in blocks.keys(): # connect left
            conn = blocks[(layer, row, col-1)]
            blocks[(layer, row, col)].left = conn

        if (layer, row, col+1) in blocks.keys(): # connect right
            conn = blocks[(layer, row, col+1)]
            blocks[(layer, row, col)].right = conn

    return blocks

def build_robot(shape3d):
    assert isinstance(shape3d, shp.Shape3D)
    assert shape3d.layers != []

    matlist = shape3d.matlist()
    blocks = init_blocks_3D(matlist)
    connected = connect_blocks_3D(blocks)

    return Robot(connected)

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

# UNUSED
# def connect_right_left(line):
#     blocks = dict()

#     for i in range(len(line)):
#         if line[i] == 1:
#             blocks[i] = Block(chr(i))

#     for pos in blocks.keys():

#         if (pos + 1) in blocks.keys():

#             rightblock = blocks[pos+1]
#             blocks[pos].right = rightblock

#         if (pos - 1) in blocks.keys():
#             leftblock = blocks[pos-1]
#             blocks[pos].left = leftblock

#     return blocks
