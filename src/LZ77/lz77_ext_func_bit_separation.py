###################################################################################
#Name: lz77_ext_func_bit_separation.py
#Description: contain class lz77 compression with bit separation mode
###################################################################################
import sys,os
sys.path.append("..")
from External_func import *
from my_LZ77 import LZ77
from operator import itemgetter
from lz77_ext_func_delimiter import LZ77_delimiter_separate

class LZ77_bit_separate(LZ77_delimiter_separate):

    def __init__(self,data,train_set,title,fast_mode=True,max_seq_bits=[5,6],window_size_bits=[17,18],debug=False):
        LZ77_delimiter_separate.__init__(self,data,train_set,title,fast_mode,max_seq_bits,window_size_bits,debug)
        self.min_sequence_arr  = [3, 5, 7] if not self.fast_mode else [3]

   ###################################################################################
    #Caculate the size in kb of compressed data
    ###################################################################################
    def data_compressed_length(self,compressed_data_no_literal,lz77):
        char_size=8
        if (self.debug):
            data_size = len(compressed_data_no_literal)*(char_size+1)\
                        + lz77.literal_num *(1+lz77.window_size_bits+lz77.sequence_length_bits)
        else:
            res = len(compressed_data_no_literal) % 8 if (len(compressed_data_no_literal) % 8) else 8
            data_size=(len(lz77.decode_binary_string(compressed_data_no_literal)) - 1) * 8 + res + \
                       lz77.literal_num * (1 + lz77.window_size_bits + lz77.sequence_length_bits)
        data_size_kb = size_KB(data_size)
        paramaters= ('data_size[KB]:', data_size_kb, \
                    'min_sequence', lz77.min_sequence, \
                    'max_sequence[bits]:', lz77.sequence_length_bits, \
                    'window_size[bits]', lz77.window_size_bits)
        return paramaters

    ###################################################################################
    #create file to save
    ###################################################################################
    def create_compress_file(self,data, control,offset_high,offset_low,length, paramater, title):
        title = (title.split())[-1]
        if not os.path.exists("..\\output\\lz_split_data_control\\" + title):
            os.makedirs("..\\output\\lz_split_data_control\\" + title)
        lib_name="..\\output\\lz_split_data_control\\"+title+"\\" + title+"_"+str(paramater[2])+str(paramater[3])+"_"\
                 +str(paramater[4])+str(paramater[5])+"_"+str(paramater[6])+str(paramater[7])
        lib_name=(lib_name.replace(':','')).replace('[bits]','bits_')
        if not os.path.exists(lib_name):
            os.makedirs(lib_name)

        self.create_compress_one_file(data,lib_name,"data")
        self.create_compress_one_file(control, lib_name, "control")
        self.create_compress_one_file(offset_high, lib_name, "offset_high")
        self.create_compress_one_file(offset_low, lib_name, "offset_low")
        self.create_compress_one_file(length, lib_name, "length")
    ###################################################################################
    # create file to save
    ###################################################################################
    def create_compress_one_file(self,data,lib_name,f_name):

        file = open(lib_name+ '\\' + f_name+ '.txt','wb')
        file.write(data)
        file.close()



