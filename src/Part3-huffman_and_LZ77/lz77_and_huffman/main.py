import sys
sys.path.append('..\..')
sys.path.append('..\..\LZ77')
sys.path.append('..\..\huffman')
from External_func import *
from huffman_and_lz77_ext_func import LZ77_huffman

#################################
### main
#################################
data_file=['..\..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1.json',
            '..\..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1.csv',
           '..\..\..\modified_data_sets\\nyc2016\\april2016_v1.csv']
train_set_file=['..\..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1_train_set.dat',
                '..\..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1_train_set.dat',
                '..\..\..\modified_data_sets\\nyc2016\\april2016_v1_train_set.dat']
title=['Location_History_102014',
       'runOrWalk',
       'nyc2016-april2016_v1']
max_seq_bits=[[5,6],[5,6],[5,6]] #for fast mode  decide the range values for max_seq bits(length)
window_size_bits_s=[[13,14],[17,18],[17,18]]#for fast mode  decide the range values for window_size bits(offset)

debug=False      #Debug mode -choose the way data compressed displayed
Fast_mode = True #Don't try all options of bit separation mode -use the cfg paramter above

for i in range(len(data_file)):
    figure_i=i
    lz77_and_huff = LZ77_huffman(data_file[i], train_set_file[i], "LZ77+Huffman compression: " + title[i],
                                 Fast_mode,max_seq_bits[i],window_size_bits_s[i])
    lz77_and_huff.lz77_and_huffman_compression(figure_i)

plt.show()

