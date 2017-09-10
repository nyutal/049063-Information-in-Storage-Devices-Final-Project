import sys
sys.path.append("..")
from collections import Counter
from Huffman import Huffman
from External_func import *
#################################################################
# calculate the most common words in train set and replace it
# with char in data and training set return also the size of this dictionary
##################################################################
def most_common_words(train_set,data,N):
    words=train_set.split(',')
    common= Counter(words).most_common()
    #print common
    dictionary=[]
    dictionary_size=0
    counter_idx = 0
    i=0
    while i < N:
        if len(common[counter_idx][0])<2:
            counter_idx += 1
            continue
        dictionary.append([common[counter_idx][0],chr(34+i)])
        data=data.replace(common[counter_idx][0],chr(34+i))
        train_set=train_set.replace(common[counter_idx][0],chr(34+i))
        if len(common[counter_idx][0]) > 0 :
            dictionary_size += (8+len(common[counter_idx][0])*8)
        counter_idx += 1
        i += 1
    print "Replacing ",N,"Common strings:"
    if (N != 0):
        pprint_code(dictionary)
    return data,train_set,size_KB(dictionary_size)

#####################################################################################################################
#calculate hofman coding(per char) for  data_set according to data_set_training and check the size of compressed data
# N1/N2/N3 -conrtol the number of most common symbol(more than 2 character) to use in hufmman code
#####################################################################################################################
def huffman_coding_compressed(data_set,data_set_train,title,figure_i,N1,N2,N3):
    huff = Huffman()
    N=[N1,N2,N3] #number of most common value replace
    data_size=[]

    data=conv_file2str(data_set)
    train_set=conv_file2str(data_set_train)
    data_size.append(len(data)*8)

    for i in N:
        [data_n,train_set_n,dictionary_size]=most_common_words(train_set,data,i)
        huff.generate_code(train_set_n)
        code = huff.encode(data_n)
        #print code
        #decode = huff.decode(code)
        data_size.append(len(code)+huff.get_dict_size()+dictionary_size)
    data_size_kb=[size_KB(x) for x in data_size ]
    #print "data_size[KB]:",data_size_kb

    labels=["Original Data" , "huffman- input alphabet1" ,\
                        "huffman- input alphabet2" , "huffman- input alphabet3"]
    plot(data_size_kb,title,labels,figure_i)
    #print decode

