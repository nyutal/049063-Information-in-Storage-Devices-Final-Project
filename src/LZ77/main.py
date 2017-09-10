import sys
sys.path.append("..")
from External_func import *
from lz77_ext_func_bit_separation import LZ77_bit_separate
from lz77_ext_func_delimiter import LZ77_delimiter_separate

######################################
### main
### using LZ77 in bit seperation mode 
######################################

data_file=['..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1.json',
            '..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1.csv',
           '..\..\modified_data_sets\\nyc2016\\april2016_v1.csv']
train_set_file=['..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1_train_set.dat',
                '..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1_train_set.dat',
                '..\..\modified_data_sets\\nyc2016\\april2016_v1_train_set.dat']
title=['Location_History_102014',
       'runOrWalk',
       'nyc2016- april2016_v1']
max_seq_bits=[[5,6],[5,6],[5,6]] #for fast mode  decide the range values for max_seq bits(length)
window_size_bits_s=[[13,14],[17,18],[17,18]]#for fast mode  decide the range values for window_size bits(offset)
window_size_bits_d=[[12,13],[18,19],[18,19]]#for fast mode  decide the range values for window_size bits(offset)

debug=True  #Debug mode -choose the way data compressed displayed
Fast_mode =True #Don't try all options of bit separation mode -use the cfg paramter above

for i in [0]:#range(len(data_file)):
    figure_i=2*i
    lz77_bit=LZ77_bit_separate(data_file[i],train_set_file[i],"LZ77 Compression (bit separation): "+title[i],Fast_mode,
                               max_seq_bits[i],window_size_bits_s[i],debug)
    lz77_bit.perform_compression_statistics(figure_i)

    lz77_delim=LZ77_delimiter_separate( data_file[i],train_set_file[i],"LZ77 Compression (delimiter separation): "+title[i],
                                        Fast_mode,max_seq_bits[i], window_size_bits_d[i])
    lz77_delim.perform_compression_statistics(figure_i+1)
plt.show()
