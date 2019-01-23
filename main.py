#!/bin/python3


import blockChainLib as bl

if __name__ == "__main__":

    bl.initBlock()
    bl.addNewBlock("hello world")
    bl.addNewBlock("hello world 2")
    bl.getAllBlocks()