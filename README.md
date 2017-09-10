# 0943063 Final Project - Compressing Data sets For machine Learning

This repository contains all the final project content.  
Final html report located at ./docs/final_project.html, it translated from our main jupyter notebook which located under src/final_project.ipynb.  
The html report need some png links from the repo, and the notebook need a lot of resource from the repo such the data set, hence download just those files will not works well, please download all.  
both the html and the notebook contains button on the top of the document which hide/show code. the code add a lot of lines and for first read we recommend hiding the code.



### Repository structure
**./data_sets:** The data sets before reformatting  
**./modified_data_sets:** The data sets after reformatting  
**./docs:** The project guide and the final report html  
**./output:** code output such graphs, LZ output for the GZIP process etc.  
**./src:** project code, include the jupyter notebook

### Execution Hows To
##### Huffman
1. enter huffman directory:  
`cd src/huffman`
2. run following command with given data_set_path:  
`python run_huffman.py <data_set_path>`

##### LZ77

##### GZIP

##### Clustered Huffman
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
