import sys,csv,re
sys.path.append('..\..')
sys.path.append("..\lz77_and_huffman_split_data_control")
from External_func import *
from huffman_and_lz77_data_control_ext_func import LZ77_huffman_data_control

class separate_columns_compress(LZ77_huffman_data_control):
    def __init__(self,data,train_set,title,fast_mode=True,max_seq_bits=[5,6],window_size_bits=[18,19],equal=True,debug=False,min_seq=[3]):
        LZ77_huffman_data_control.__init__(self,data,train_set,title,fast_mode,max_seq_bits,window_size_bits,min_seq,debug)
        self.equal=equal
    #########################################################
    #this function return the maximum column size in each file
    ##########################################################
    def find_col_size(self,file):
            max_line=0
            with open(file) as fp:
             for line in fp:
                if (self.equal):
                    del_i=re.sub("[0-9a-zA-Z]+", "", line)
                    del_i=del_i.replace(',-',',')
                else:
                    del_i=','*(line.count(',')+1)
                if len(del_i)>max_line:
                    max_line=len(del_i)
                    delimiter=del_i

            print max_line,delimiter
            return max_line,delimiter

    ##########################################################
    #function separate the column of the file
    ##########################################################
    def separate_columns(self,file,col_num,delimiter):
        columns = [[] for x in xrange(col_num)]
        with open(file, 'r') as f:
            if not (self.equal):
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    for i in range(col_num):
                        columns[i].append(row[i] if i < len(row) else '')

                #reader = csv.reader(f, delimiter='-')
                #for row in reader:
            else:
                 for line in f:
                    for n in range (col_num):
                        line=str(line)
                        line=line.split(delimiter[n],1)
                        columns[n].append(line[0]if 0 <len(line) else ',')
                        line=(line[1] if 1 < len(line) else line)

        for i in range(col_num):
            columns[i]=str(columns[i]).replace('\'','')
            #print "columns ",i,":",columns[i]
        return columns

    ##########################################################################
    #function call hufmann compression for each column and
    # return the total data size
    ########################################################################
    def separate_lines_huff_compress(self,columns_data,columns_train_set,col_num):
        huff_size=0
        for i in range(col_num):
            size = self.huff_compress(columns_data[i], columns_train_set[i])
            print "huff_size :column", i, " :",size
            huff_size+=size
        return  huff_size

    ##########################################################################
    #function call lz77 and hufmann compression for each column and
    #return the total data size of lz77 and lz7&huff compression
    ##########################################################################
    def separate_lines_lz77_huff_compress(self,columns_data,columns_train_set,col_num):

        lz77_size_min=0
        lz77_and_huff_size_min=0
        for i in range(col_num):
            uncompressed_data_size, min_parameters = self.find_paramter_to_compress(3)
            lz77_size = []
            lz77_and_huffman_size= []

            lz77_size.append(size_KB(len(columns_data[i]) * 8))

            for paramater in min_parameters:
                # first compression with lz77
                data, control, offset_high,offset_low ,length= self.compress_lz77(columns_data[i], paramater)
                lz77_size.append(size_KB(len(data+control+offset_high+offset_low+length)*8+2)) #2 is for column mara data(lz77 paramters,columns separarions)
                # second compression with huffman
                lz77_and_huffman_size.append(self.huff_compress(data, data) + self.huff_compress(control, control)+ \
                                             self.huff_compress(offset_high, offset_high) + self.huff_compress(offset_low, offset_low) + \
                                             self.huff_compress(length, length))
                # second compression with huffman


            print "lz77_size :column",i," :",min(lz77_size)
            lz77_size_min+=min(lz77_size)
            #print "lz77_and_huffman_size :column", i, " :", lz77_and_huffman_size, " min: ", min(lz77_and_huffman_size)
            lz77_and_huff_size_min += min(lz77_and_huffman_size)

        return lz77_size_min,lz77_and_huff_size_min

    ##########################################################################
    #compress eaxh file by column using huffman and lz77
    ###############################################################
    def separate_columns_compression(self,figure_i):
        col_num,delimiter=self.find_col_size(self.data)
        columns_train_set=self.separate_columns(self.train_set,col_num,delimiter)
        columns_data=self.separate_columns(self.data,col_num,delimiter)

        uncompressed_data_size=sum([size_KB(len(data)*8) for data in columns_data])
        huff_size=self.separate_lines_huff_compress(columns_data,columns_train_set,col_num)
        lz77_size,lz77_and_huffman_size =self.separate_lines_lz77_huff_compress(columns_data,columns_train_set, col_num)

        data=[uncompressed_data_size,huff_size,lz77_size,lz77_and_huffman_size]
        labels=["Original Data","huffman_size" ,"lz77_size","lz77_and_huffman"]
        plot(data,self.title,labels,figure_i)
