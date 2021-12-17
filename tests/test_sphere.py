



import sys
sys.path.append("..") # Adds higher directory to python modules path.

import to_bip as tb
import blocks as bl
import shapegen as sh

def main():
      print("---- Sphere ----")
      sphere = sh.Sphere(5)
      sphere.generate()
      sphere_blocks = bl.init_blocks_3D(sphere.matlist())
      sphere_conn = bl.connect_blocks_3D(sphere_blocks)

      print("LAYERS:")
      for mat in sphere.matlist():
          bl.print_matrix(mat)
          print("\n")
      print("\n")

      for block in sphere_conn.values():
          bl.visual_print_2D(block)
          print("\n")

      tb.write_BIP("sphere.bip", sphere_conn)

if __name__ == "__main__":
    main()
