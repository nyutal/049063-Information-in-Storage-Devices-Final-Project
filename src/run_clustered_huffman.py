import sys
import os
import itertools

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './clustered_huffman')))
import clustered_huffman
from clustered_huffman_cfg import ClusteredHuffmanCfg


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('ERROR: "run_clustered_huffman.py <data set file>"')
    if not os.path.isfile(sys.argv[1]):
        sys.exit('ERROR: no exists path!, "run_clustered_huffman.py <data set file>"')
        # print 'ERROR: run_huffman.py <data set file>'
    ch = clustered_huffman.ClusteredHuffman(\
        sample_seperator=ClusteredHuffmanCfg.sample_seperator,\
        train_batch_size=ClusteredHuffmanCfg.train_batch_size, \
        n_clusters=ClusteredHuffmanCfg.n_clusters,\
        train_fraction=ClusteredHuffmanCfg.train_fraction,\
        verbose=ClusteredHuffmanCfg.verbose\
    )
    ch.build_codes(sys.argv[1])
    ch.print_compression_info_file(sys.argv[1], ClusteredHuffmanCfg.encode_batch_size)
    print 'by'