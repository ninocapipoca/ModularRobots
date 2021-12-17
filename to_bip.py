import shapegen as shp
import randomgen as rd
import blocks as bl

# Unfortunately this is incomplete and will not produce a fully functional BIP file
# But the idea is this, a couple of details are just missing

def write_BIP(filename, blocks):
    assert isinstance(filename, str)
    if filename[-4:] != ".bip":
        filename = filename + ".bip"
        
    
    bipfile = open(filename, "w")
    bipfile.write("package shape\n"
                  + "\tuse BlinkyBlockCable\n"
                  + "\tuse BlinkyBlock\n"
                  + "\tuse ports\n")
    bipfile.write("\n")
    bipfile.write("\tcompound type shape()\n\n") 


    # create the block instances
    # connect them if applicable
    for bl.block in blocks.values():
        bipfile.write(bl.block.BIP_instance() + "\n")
        bipfile.write(bl.block.BIP_connect_front() + "\n")
        bipfile.write(bl.block.BIP_connect_back() + "\n")
        bipfile.write(bl.block.BIP_connect_left() + "\n")
        bipfile.write(bl.block.BIP_connect_right() + "\n")
        bipfile.write(bl.block.BIP_connect_top() + "\n")
        bipfile.write(bl.block.BIP_connect_bottom() + "\n")
    

    bipfile.write("\tend\n")
    bipfile.write("end")
    
    bipfile.close() 
