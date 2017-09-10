import sys
sys.path.append('..\..')
sys.path.append('..\..\LZ77')
sys.path.append('..\..\huffman')
sys.path.append('..\lz77_and_huffman')
from External_func import *
from my_LZ77 import LZ77
from operator import itemgetter
from huffman_and_lz77_ext_func import LZ77_huffman


class LZ77_data_control(LZ77):
    ###################################################################################
    #compress lz77 but separate the data
    ###################################################################################
    def compress(self, data, debug=None):
        compressed_data = ''
        compressed_control = ''
        compressed_offset_high = ''
        compressed_offset_low = ''
        compressed_length = ''
        window = ''

        i = 0
        while i < len(data):
            seq_len = 1
            while i + seq_len <= len(data) and seq_len <= self.max_sequence and data[i:i + seq_len] in window:
                seq_len += 1

            seq_len -= 1
            if seq_len >= self.min_sequence and data[i:i + seq_len] in window:
                offset = len(window) - window.rfind(data[i:i + seq_len])
                compressed_control += '1'
                compressed_offset_high += self.offset_format.format(offset)[0:8]
                if (self.window_size_bits>8):
                    compressed_offset_low += self.offset_format.format(offset)[8:]
                else:
                    compressed_offset_low='0' #nit exist in this case
                compressed_length += self.length_format.format(seq_len)
                window += data[i:i + seq_len]
                i += seq_len
            else:
                compressed_control += '0'
                compressed_data += data[i]
                window += data[i]
                i += 1

            window = window[-self.window_size:]

        compressed_control = self.decode_binary_string(compressed_control)
        compressed_length = self.decode_binary_string(compressed_length)
        compressed_offset_high = self.decode_binary_string(compressed_offset_high)
        compressed_offset_low = self.decode_binary_string(compressed_offset_low)

        return compressed_data, compressed_control, compressed_offset_high, compressed_offset_low, compressed_length

class LZ77_huffman_data_control(LZ77_huffman):
    def __init__(self,data,train_set,title,fast_mode=True,max_seq_bits=[5,6],window_size_bits=[17,18],min_seq=[3],debug=False):
        LZ77_huffman.__init__(self,data,train_set,title,fast_mode,max_seq_bits,window_size_bits,debug)
        self.min_sequence_arr  = [3, 5, 7] if not self.fast_mode else min_seq

    ###################################################################################
    #Caculate the size in kb of lz77 compressed data+control
    ###################################################################################
    def lz77_data_control_compressed_length(self,data,control,lz77):
        char_size=8
        data_size = len(data+control)*char_size
        data_size_kb = size_KB(data_size)
        paramaters= (('data_size[KB]:', data_size_kb, \
                    'min sequence', lz77.min_sequence, \
                    'max_sequence[bits]:', lz77.sequence_length_bits, \
                    'window_size[bits]', lz77.window_size_bits))
        return paramaters

    #convert binary stream to sring
    def decode_binary_string(self,s):
        str=''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)/8))
        return str if (len(s)%8 == 0) else str+(chr(int(s[-(len(s)%8):],2)))


    ###################################################################################
    # compress with  LZ77 and paramter provided return data and control compressed
    ###################################################################################
    def compress_lz77(self,data_s,paramater):
        min_sequence = paramater[3]
        max_sequence_bits = paramater[5]
        window_size_bits = paramater[7]

        lz77_i = LZ77_data_control(min_sequence, max_sequence_bits, window_size_bits)
        data, control,offset_high,offset_low,length= lz77_i.compress(data_s)
        data_size_paramater = self.lz77_data_control_compressed_length(data, control+offset_high+offset_low+length, lz77_i)
        return data, control,offset_high,offset_low,length

    ###################################################################################
    #compressin the data using LZ77 and hufmman algorithm
    ##################################################################################
    def lz77_and_huffman_compression(self,figure_i):
        data_size_kb=[]
        parameter_size_arr=[]

        print "Starting compression for (data+control) : "+self.title
        ### Training set - finding min paramater
        print "For training set resualt"
        uncompressed_data_size,min_parameters=self.find_paramter_to_compress(4)

        ### Data set- compress data set using the paramter we find in the training set
       #original data
        data_s = conv_file2str(self.data)
        data_size_kb.append(size_KB(len(data_s) * 8))
        print "uncompressed_data_size",data_size_kb[0]

        for paramater in min_parameters:
            #first compression with lz77
            data, control, offset_high,offset_low, length=self.compress_lz77(data_s,paramater)
            self.create_compress_file(data, control,offset_high,offset_low,length, paramater,self.title)
            data_size=( self.huff_compress(data,data)+self.huff_compress(control,control)+\
                        self.huff_compress(offset_high,offset_high)+ self.huff_compress(offset_low,offset_low)+\
                        self.huff_compress(length,length))
            parameter_size_arr.append([data_size, paramater])

        parameter_size_arr.sort(key=itemgetter(0), reverse=True)
        for x in parameter_size_arr:
            data_size_kb.append(x[0])
        #plt
        labels=["Original Data"]+[str(x[1][2::1]) for x in parameter_size_arr]
        plot(data_size_kb,self.title,labels,figure_i)
