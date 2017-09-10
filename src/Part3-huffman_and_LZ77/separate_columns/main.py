import sys
sys.path.append('..\..')
sys.path.append("..\lz77_and_huffman")
from External_func import *
from separate_column_ext_func import separate_columns_compress
#################################
### main
#################################
data_file=['..\..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1_columns.dat',
            '..\..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1.csv',
           '..\..\..\modified_data_sets\\nyc2016\\april2016_v1.csv']
train_set_file=['..\..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1_columns_train_set.dat',
                '..\..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1_train_set.dat',
                '..\..\..\modified_data_sets\\nyc2016\\april2016_v1_train_set.dat']
title=['Location_History_102014',
       'runOrWalk',
       'nyc2016- april2016_v1']

max_seq_bits=[[5,6],[5,6],[5,6]] #for fast mode  decide the range values for max_seq bits(length)
window_size_bits_s=[[13,14],[17,18],[17,18]]#for fast mode  decide the range values for window_size bits(offset)
equal=[False,True,True] #set the algorithm wto work with data set that All columns are of equal length

debug=False #Debug mode -choose the way data compressed displayed
Fast_mode = True #Don't try all options of bit separation mode -use the cfg parameter above

for i in range (len(data_file)):
    figure_i=i
    compress = separate_columns_compress(data_file[i], train_set_file[i], "LZ77+Huffman compression (split columns): " + title[i],
                                    Fast_mode, max_seq_bits[i], window_size_bits_s[i],equal[i])
    compress.separate_columns_compression(figure_i)

plt.show()


