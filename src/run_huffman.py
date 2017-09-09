import sys
import os
import itertools

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './huffman')))
import Huffman


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('ERROR: "run_huffman.py <data set file>"')
    if not os.path.isfile(sys.argv[1]):
        sys.exit('ERROR: no exists path!, "run_huffman.py <data set file>"')
        # print 'ERROR: run_huffman.py <data set file>
    h = Huffman.Huffman()
    h.generate_code(itertools.chain.from_iterable(open(sys.argv[1])))
    h_2_uc, h_2_c, _ = h.print_compression_info_file(sys.argv[1])
