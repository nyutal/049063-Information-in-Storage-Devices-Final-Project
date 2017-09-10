from huffman_ext_func import *
#################################
##main
#################################
N1=0 # N1/N2/N3 -conrtol the number of most common symbol(more than 2 character) to use in hufmman code
N2=5
N3=10

data_file=['..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1.json',
           '..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1.csv',
           '..\..\modified_data_sets\\nyc2016\\april2016_v1.csv']
train_set_file=['..\..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1_train_set.dat',
                '..\..\modified_data_sets\\runOrWalk\\runOrWalk_v1_train_set.dat',
                '..\..\modified_data_sets\\nyc2016\\april2016_v1_train_set.dat']
title=['Location_History_102014',
       'runOrWalk',
       'nyc2016- april2016_v1']

for i in range (len(data_file)):
    figure_i=i
    huffman_coding_compressed(data_file[i], train_set_file[i],"Huffman compression: " +title[i], figure_i, \
                              N1, N2, N3)
plt.show()
