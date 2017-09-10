import sys
sys.path.append('..\..')
sys.path.append('..\..\LZ77')
sys.path.append('..\..\huffman')
from External_func import *
from huffman_ext_func import Huffman
from my_LZ77 import LZ77
from operator import itemgetter
from lz77_ext_func_bit_separation import LZ77_bit_separate


class LZ77_huffman(LZ77_bit_separate):
    ###################################################################################
    # compress data  with huffman algorithm return data size
    ###################################################################################
    def huff_compress(self,data_compressed,train_set):
        huff = Huffman()
        huff.generate_code(data_compressed)
        code = huff.encode(data_compressed)
        data_size=len(code) + huff.get_dict_size()
        return size_KB(data_size)

    ###################################################################################
    # compress with  LZ77 and paramter provided return data compressed
    ###################################################################################
    def compress_lz77(self,data_s,paramater):
        min_sequence = paramater[3]
        max_sequence_bits = paramater[5]
        window_size_bits = paramater[7]

        lz77 = LZ77(min_sequence, max_sequence_bits, window_size_bits)
        data_compressed, compressed_data_no_literal = lz77.compress(data_s,self.debug)
        data_size_paramater = self.data_compressed_length(compressed_data_no_literal, lz77)

        print "after LZ77 data size:", data_size_paramater
        data_compressed = lz77.decode_binary_string(data_compressed)
        return data_compressed

    ###################################################################################
    #compressin the data using LZ77 and hufmman algorithm
    ##################################################################################
    def lz77_and_huffman_compression(self,figure_i):
        parameter_size_arr=[]
        data_size_kb=[]

        print "Starting : "+self.title
        ### Training set - finding min paramater
        #print "For training set resualt"
        uncompressed_data_size,min_parameters=self.find_paramter_to_compress(3)

        ### Data set- compress data set using the paramter we find in the training set
       #original data
        data_s = conv_file2str(self.data)
        data_size_kb.append(size_KB(len(data_s) * 8))
        #print "uncompressed_data_size",data_size_kb[0]

        for paramater in min_parameters:
            #first compression with lz77
            data_compressed=self.compress_lz77(data_s,paramater)
            #print data_compressed

            #second compression with huffman
            parameter_size_arr.append([self.huff_compress(data_compressed,data_compressed),paramater])

        parameter_size_arr.sort(key=itemgetter(0),reverse=True)
        for x in parameter_size_arr:
            data_size_kb.append(x[0])
        #plt
        labels=["Original Data"]+[str(x[1][2::1]) for x in parameter_size_arr]
        plot(data_size_kb,self.title,labels,figure_i)
