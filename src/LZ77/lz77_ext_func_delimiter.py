###################################################################################
#Name: lz77_ext_func_delimiter.py
#Description: contain class  lz77 compression with symbole delimiter mode
###################################################################################
import sys
sys.path.append("..")
from my_LZ77 import LZ77
from operator import itemgetter
from External_func import *

class LZ77_delimiter_separate(object):
    def __init__(self,data,train_set,title,fast_mode=True,max_seq_bits=[5,6],window_size_bits=[18,19],debug=True):
        self.data      = data
        self.train_set = train_set
        self.title     = title
        self.fast_mode = fast_mode
        self.debug     = debug
        self.max_sequence_bits_arr = range(3,10)  if not self.fast_mode else range(max_seq_bits[0],max_seq_bits[1]+1)#range(4,8) : run or work :5 history :6
        self.window_size_bits_arr  = range(7,25)  if not self.fast_mode else range(window_size_bits[0],window_size_bits[1]+1)#range(10,15) run or work:18,19  history 12,13
        self.min_sequence_arr  = [3, 5, 7] if not self.fast_mode else [3,5]
    ###################################################################################
    #Caculate the size in kb of compressed data
    ###################################################################################
    def data_compressed_length(self,compressed_data_no_literal,lz77):
        char_size=8
        data_size = len(compressed_data_no_literal)*char_size +\
                    lz77.literal_num *(char_size+lz77.window_size_bits+lz77.sequence_length_bits)
        data_size_kb = size_KB(data_size)
        paramaters= (('data_size[KB]:', data_size_kb, \
                    'min sequence', lz77.min_sequence, \
                    'max_sequence[bits]:', lz77.sequence_length_bits, \
                    'window_size[bits]', lz77.window_size_bits))
        return paramaters

    ###################################################################################
    #finding the best parameter for compressed accordint the train_set using lz77
    ###################################################################################
    def find_paramter_to_compress(self,p_num):
        data_size_kb_arr  = []
        train_set_s = conv_file2str(self.train_set)
        #print data

        uncompressed_data_size=size_KB(len(train_set_s) * 8)

        for min_sequence in self.min_sequence_arr:
            for max_sequence_bits in self.max_sequence_bits_arr:
                for window_size_bits in self.window_size_bits_arr:
                    lz77 = LZ77(min_sequence,max_sequence_bits,window_size_bits)

                    data_compressed,compressed_data_no_literal= lz77.compress(train_set_s,self.debug)
                    #print data_compressed
                    #print compressed_data_no_literal
                    data_size_paramater= self.data_compressed_length(compressed_data_no_literal,lz77)
                    data_size_kb_arr.append(data_size_paramater)

        data_size_kb_arr.sort(key=itemgetter(1))
        #for i in data_size_kb_arr: print i
        return uncompressed_data_size,data_size_kb_arr[:p_num]


    ###################################################################################
    #compressin the data according the paramaters we find with the train_set
    ###################################################################################
    def data_compressed(self,min_parameters):
        data_size_kb_arr=[]

        data_s = conv_file2str(self.data)
        uncompressed_data_size=round((len(data_s) * 8)/8192.0, 2)
        #print data

        for paramater in min_parameters:
            min_sequence=paramater[3]
            max_sequence_bits=paramater[5]
            window_size_bits= paramater[7]

            lz77 = LZ77(min_sequence, max_sequence_bits,window_size_bits)
            data_compressed, compressed_data_no_literal = lz77.compress(data_s, self.debug)
            data_size_paramater= self.data_compressed_length(compressed_data_no_literal,lz77)

            data_size_kb_arr.append(data_size_paramater)
        return  data_size_kb_arr,uncompressed_data_size
    ###################################################################################
    #lot the compression statistics
    ###################################################################################
    def plot_result(self,uncompressed_data_size,data_param_arr,figure_i):
        data_param_arr.sort(key=itemgetter(1),reverse=True)
        labels=["Original Data"]+[str(x) for x in data_param_arr]
        data_size=[uncompressed_data_size ]+[x[1] for x in data_param_arr]
        plot(data_size,self.title,labels,figure_i)

    ###################################################################################
    #perform lz77 compression (symbole delimiter mode) on data
    ###################################################################################
    def perform_compression_statistics(self,figure_i):

        print "Starting " + self.title
        ### Training set - finding min paramater
        uncompressed_data_size,min_parameters=self.find_paramter_to_compress(3)
        #print "For training set resualt"
        #print "uncompressed_data_size: ",uncompressed_data_size,"[KB]"
        #for i in min_parameters: print i

        ### Data set- compress data set using the paramter we find in the training set
        data_param_arr,uncompressed_data_size=self.data_compressed(min_parameters)
        #print "For Data set resualt"
        #print "uncompressed_data_size: ",uncompressed_data_size,"[KB]"
        #for i in data_param_arr:  print i

        #plot the result
        self.plot_result(uncompressed_data_size, data_param_arr,figure_i)


