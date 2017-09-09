import math


class LZ77(object):
    def __init__(self, min_sequence, sequence_length_bits, window_size_bits):
        self.min_sequence = min_sequence
        self.sequence_length_bits = sequence_length_bits
        self.max_sequence = pow(2, sequence_length_bits) + self.min_sequence - 1
        self.window_size_bits = int(window_size_bits)
        self.window_size = pow(2, window_size_bits) - 1
        self.length_format = '{:0%sb}' % sequence_length_bits
        self.offset_format = '{:0%sb}' % window_size_bits

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
                compressed_offset_low += self.offset_format.format(offset)[8:]
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

    # convert binary stream to sring
    def decode_binary_string(self, s):
        str = ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) / 8))
        return str if (len(s) % 8 == 0) else str + (chr(int(s[-(len(s) % 8):], 2)))