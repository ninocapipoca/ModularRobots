
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import to_bip as tb
import blocks as bl
import shapegen as sh

def main():
      print("---- Triangle ----")
      triangle = sh.Triangle(5)
      triangle.generate()
      triangle_blocks = bl.init_blocks_2D(triangle.mat)
      triangle_conn = bl.connect_blocks_2D(triangle_blocks)
      bl.print_matrix(triangle.mat)
      print("\n")

      for block in triangle_conn.values():
          bl.visual_print_2D(block)

      tb.write_BIP("triangle.bip", triangle_conn)
if __name__ == "__main__":
    main()
