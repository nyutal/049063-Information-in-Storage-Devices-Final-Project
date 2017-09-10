# 0943063 Final Project - Compressing Data sets For machine Learning

This repository contains all the final project content.  
Final html report located at ./docs/final_project.html
It is translated from our main jupyter notebook which located under src/final_project.ipynb.  
The html report needs some png links from the repo, and the notebook needs a lot of resource from the repo such the data set,
hence download just those files will not works well, please download all the repository.  
both the html and the notebook contains button on the top of the document which hide/show code.
The code add a lot of lines and for first read we recommend hiding the code.



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
1. Create train set with create_training_set method with data_set_path(incase you need):
`cd src`
`python -c 'import External_func; print External_func.create_training_set("data_set_path")'

2. enter LZ77 directory:  
`cd src/LZ77`

3. edit the main file with desired  parameters:
	data_file=["data_file_path"]
	train_set_file=["train_set_file"]
	title=["Plot title"]
	max_seq_bits=[5,6]          #control the range values for max_seq bits(length) in LZ77
	window_size_bits_s=[17,18]  #control the range values for window_size bits(offset) in LZ77- bit separation mode
	window_size_bits_d=[12,13]  #control the range values for window_size bits(offset) in LZ77- delimiter mode
4. run the main file:  
`python main.py`

##### GZIP
###### LZ77+Huffman
1. Create train set with create_training_set method with data_set_path(incase you need):
`cd src`
`python -c 'import External_func; print External_func.create_training_set("data_set_path")'

2. enter LZ77 directory:  
`cd src/Part3-huffman_and_LZ77/lz77_and_huffman`

3. edit the main file with desired  parameters:
	data_file=["data_file_path"]
	train_set_file=["train_set_file"]
	title=["Plot title"]
	max_seq_bits=[5,6]          #control the range values for max_seq bits(length) in LZ77
	window_size_bits_s=[17,18]  #control the range values for window_size bits(offset) in LZ77- bit separation mode

4. run the main file:  
`python main.py`

###### LZ77 (split data,control,offset_high,offset_low,length )+Huffman
1. Create train set with create_training_set method with data_set_path(incase you need):
`cd src`
`python -c 'import External_func; print External_func.create_training_set("data_set_path")'

2. enter LZ77 directory:  
`cd src/Part3-huffman_and_LZ77/lz77_and_huffman_split_data_control`

3. edit the main file with desired  parameters:
	data_file=["data_file_path"]
	train_set_file=["train_set_file"]
	title=["Plot title"]
	max_seq_bits=[5,6]          #control the range values for max_seq bits(length) in LZ77
	window_size_bits_s=[17,18]  #control the range values for window_size bits(offset) in LZ77- bit separation mode
	min_seq=[4,5,6]             #control the minimum sequence that LZ77  start to copy

4. run the main file:  
`python main.py`

###### LZ77 (separation columns) + Huffman  
1. Create train set with create_training_set method with data_set_path(incase you need):
`cd src`
`python -c 'import External_func; print External_func.create_training_set("data_set_path")'

2. enter LZ77 directory:  
`cd src/Part3-huffman_and_LZ77/separate_columns`

3. edit the main file with desired  parameters:
	data_file=["data_file_path"]
	train_set_file=["train_set_file"]
	title=["Plot title"]
	max_seq_bits=[5,6]          #control the range values for max_seq bits(length) in LZ77
	window_size_bits_s=[17,18]  #control the range values for window_size bits(offset) in LZ77- bit separation mode
	equal=[True]                #set the algorithm wto work with data set that all columns are of equal length

4. run the main file:  
`python main.py`

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
