# Final Project Execution Hows To
## Huffman
1. enter huffman directory:  
`cd src/huffman`
2. run following command with given data_set_path:  
`python run_huffman.py <data_set_path>`

## LZ77

## GZIP

## Clustered Huffman
1. enter clustered huffman directory:  
`cd src/clustered_huffman`  
2. edit and configure desired parameters in the clustered_huffman_cfg.py:  
        sample_seperator = '\n'  
        train_batch_size = 100  
        n_clusters = 8  
        verbose = True  
        train_fraction = None  
        encode_batch_size = 100
3. run following command for given data_set_path:  
`python run_clustered_huffman.py <data_set_path>`
