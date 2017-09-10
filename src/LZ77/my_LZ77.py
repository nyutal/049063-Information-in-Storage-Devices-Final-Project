###################################################################################
#Name: LZ77.py
#Description: LZ77 compression implementation
###################################################################################
import math

class LZ77(object):
    def __init__(self, min_sequence, sequence_length_bits, window_size_bits):
        # type: (object, object) -> object
        self.min_sequence =min_sequence;
        self.sequence_length_bits = sequence_length_bits
        self.max_sequence = pow(2, sequence_length_bits)-1+ self.min_sequence
        self.window_size_bits = int(window_size_bits)
        self.window_size = pow(2, window_size_bits)-1
        self.length_format = '{:0%sb}' % sequence_length_bits
        self.offset_format = '{:0%sb}' % window_size_bits

    def compress(self, data, debug=None):
        if debug is None:
            debug = False

        compressed_data = ''
        compressed_data_no_literal = ''
        window = ''
        self.literal_num = 0

        i = 0
        while i < len(data):
            seq_len = 1
            while i + seq_len <= len(data) and seq_len <= self.max_sequence and data[i:i + seq_len] in window:
                seq_len += 1

            seq_len -= 1
            if seq_len >= self.min_sequence and data[i:i + seq_len] in window:
                offset = min(i, self.window_size) - window.rfind(data[i:i + seq_len])
                compressed_data += self.writePair(offset, seq_len, debug)
                window += data[i:i + seq_len]
                i += seq_len
            else:
                compressed_data += self.writeLitteral(data[i], debug)
                compressed_data_no_literal += self.writeLitteral(data[i], debug)
                window += data[i]
                i += 1

            window = window[-self.window_size:]
        return compressed_data, compressed_data_no_literal


    def writeLitteral(self, literal, debug):
        res = literal if debug else '0'+bin(ord(literal))[2:].zfill(8)
        #print res
        return res
    def writePair(self, offset,length, debug):
        if debug:
            res = '(' + str(length) + ',' + str(offset) + ')'
        else:
            res = '1' +self.offset_format.format(offset) + self.length_format.format(length)
        self.literal_num += 1
        return res

    #convert number to binary
    def binary(self,num, length=8):
        return format(num, 'b'.format(length+1))

    #convert binary stream to sring
    def decode_binary_string(self,s):
        str=''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)/8))
        return str if (len(s)%8 == 0) else str+(chr(int(s[-(len(s)%8):],2)))

if __name__ == "__main__":
    lz77 = LZ77(3,3,5)
    literal_size=1
    data = 'abracadabra'
    print data
    #print lz77.compress(data, True)

    data = 'Little Bunny Foo Foo \
Hopping through the forest \
Scooping up the field mice \
And boppin em on the head \
Down came the good fairy and she said \
Little Bunny Foo Foo \
I dont want to see you \
Scooping up the field mice \
And boppin em on the head \
Ill give you three chances \
And if you dont behave \
Ill turn you into a goon!'

    print "True mode:"
    data_compress, data_compress_no_literals= lz77.compress(data, True)
    print data_compress
    print data_compress_no_literals
    res = len(data_compress_no_literals) % 8 if (len(data_compress_no_literals) % 8) else 8
    print "length data compreesed with no literals ", len(data_compress_no_literals) * (8+1) \
                                                     + lz77.literal_num * (lz77.window_size_bits + lz77.sequence_length_bits + 1)
    print "False mode:"
    data_compress,data_compress_no_literals= lz77.compress(data, False)
    print data_compress
    print (len(data_compress)%8)
    data_compress_str=lz77.decode_binary_string(data_compress)
    res=len(data_compress)%8 if (len(data_compress)%8) else 8
    print "length data compreesed:",(len(data_compress_str)-1)*8 + res

    res = len(data_compress_no_literals) % 8 if (len(data_compress_no_literals) % 8) else 8
    print "length data compreesed with no literals ",(len(lz77.decode_binary_string(data_compress_no_literals))-1)*8+res + lz77.literal_num * (lz77.window_size_bits+lz77.sequence_length_bits+1)

    # print "data size:",len(data)*8,"compressed size:",(len(lz77.compress(data,True))- (3*lz77.literal_num))*9


