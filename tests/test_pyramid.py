
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import to_bip as tb
import blocks as bl
import shapegen as sh

def main():
    print(" ---- Pyramid ----")
    py = sh.Pyramid(5)
    py.generate()
    py_blocks = bl.init_blocks_3D(py.matlist())
    py_conn = bl.connect_blocks_3D(py_blocks)

    for block in py_conn.values():
        bl.visual_print_2D(block)
        print("\n")

    print("LAYERS:")
    for mat in py.matlist():
        bl.print_matrix(mat)
        print("\n")
    print("\n")

    tb.write_BIP("pyramid.bip", py_conn)


if __name__ == "__main__":
    main()
