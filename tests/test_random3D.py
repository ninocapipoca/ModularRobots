
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import to_bip as tb
import blocks as bl
import shapegen as sh
import randomgen as rand

def main():
      print("---- Random 3D ----")
      random = rand.random_shape3D(3)
      blocks = bl.init_blocks_3D(random.matlist())
      conn = bl.connect_blocks_3D(blocks)

      print("LAYERS:")
      for mat in random.matlist():
          bl.print_matrix(mat)
          print("\n")

      print("\n")

      for block in conn.values():
          bl.visual_print_2D(block)
          print("\n")

      tb.write_BIP("random_3D.bip", conn)
if __name__ == "__main__":
    main()
