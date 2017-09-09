from collections import Counter
import pandas as pd
import heapq
import itertools


class Huffman(object):
    CODE_LENGTH_BITS = 8
    HEADER = ['uncompressed[b]', 'compressed(without code)[b]', 'dictionary[b]', 'neto ratio[b]', 'total ratio[b]']

    def __init__(self, stop_chars=[]):
        self.stop_chars = stop_chars
        pass

    def generate_code(self, char_stream):
        '''
        build huffman code for given char_stream.
        it is initial step in order to compress/decompresse with this class
        '''
        # construct an heap
        counts = dict(Counter(char_stream))
        self.generate_code_from_freq_dict(counts)

    def generate_code_from_freq_dict(self, counts):
        for c in self.stop_chars:
            if c in counts:
                del counts[c]
        heap = []
        for char, freq in counts.items():
            node = {'val': char, 'left': None, 'right': None}
            heapq.heappush(heap, (freq, node))

        self.counts = counts

        # build a prefix tree
        root = self._build_tree(heap)

        # produce code
        self.code_dict = {}
        self._traverse_and_code(root, '', self.code_dict)

        # convert dict for decode performance
        self.decode_dict = {v: k for k, v in self.code_dict.iteritems()}

    def _build_tree(self, heap):
        while len(heap) > 1:
            fr1, right = heapq.heappop(heap)
            fr2, left = heapq.heappop(heap)
            node = {'left': left, 'right': right}
            heapq.heappush(heap, (fr1 + fr2, node))
        _, root = heapq.heappop(heap)
        return root

    def _traverse_and_code(self, node, prefix, code_dict):
        if 'val' in node:
            code_dict[node['val']] = prefix
        else:
            self._traverse_and_code(node['left'], (prefix + '0'), code_dict)
            self._traverse_and_code(node['right'], prefix + '1', code_dict)

    def get_code(self):
        return self.code_dict

    def set_code(self, d):
        self.code_dict = d

    def print_code(self):
        print 'Huffman code:'
        for k, v in self.code_dict.items():
            print '%s %s %s' % (k, ord(k), v)

    def pprint_code(self):
        header = ['charactter', 'ascii', 'code']
        table = []
        for k, v in self.code_dict.items():
            table.append([k, ord(k), v])
        print_table(header, table)

    def get_char_count(self):
        return self.counts

    def get_char_freq(self):
        total_counts = float(sum([count for count in self.counts.values()]))
        freq_dict = {k: v / total_counts for k, v in self.counts.items()}
        return freq_dict

    def encode(self, char_stream):
        '''
        return: string represent compressed char_stream bits
        '''
        binary_stream = ''
        for c in char_stream:
            if c not in self.code_dict:
                if c in self.stop_chars:
                    continue
                raise ValueError('%s (ord=%s) not in code_dict' % (c, ord(c)))
            binary_stream += self.code_dict[c]
        return binary_stream

    def decode(self, binary_stream):
        '''
        return char string represent uncompresed binary_stream for it's code_dict
        '''
        curr_exp = ''
        char_stream = ''

        for b in binary_stream:
            curr_exp += b
            if curr_exp in self.decode_dict:
                char_stream += self.decode_dict[curr_exp]
                curr_exp = ''

        if len(curr_exp) != 0:
            raise ValueError('wrong code!!!')

        return char_stream

    def get_dict_size(self):
        total_len = 0
        for k, v in self.code_dict.items():
            total_len += 8 * len(k) + self.CODE_LENGTH_BITS + len(v)
        return total_len

    def compression_info(self, char_stream):
        bin_stream = self.encode(char_stream)
        uncompressed_len = 0
        for c in char_stream:
            if c not in self.stop_chars:
                uncompressed_len += 8
        compressed_len = len(bin_stream)
        return uncompressed_len, compressed_len, self.get_dict_size()

    def print_compression_info(self, char_stream):
        uncompressed_len, compressed_len, dict_size = self.compression_info(char_stream)
        ratio = (dict_size + compressed_len) * 1. / uncompressed_len
        table = [[uncompressed_len, compressed_len, dict_size, compressed_len * 1. / uncompressed_len, ratio]]
        print_table(self.HEADER, table)
        return uncompressed_len, compressed_len, dict_size

    def compression_info_file(self, fname):
        bin_stream = self.encode(itertools.chain.from_iterable(open(fname)))

        uncompressed_len = 0
        for c in itertools.chain.from_iterable(open(fname)):
            if c not in self.stop_chars:
                uncompressed_len += 8

        compressed_len = len(bin_stream)

        return uncompressed_len, compressed_len, self.get_dict_size()

    def print_compression_info_file(self, fname):
        uncompressed_len, compressed_len, dict_size = self.compression_info_file(fname)
        ratio = (self.get_dict_size() + compressed_len) * 1. / uncompressed_len
        table = [[uncompressed_len, compressed_len, dict_size, compressed_len * 1. / uncompressed_len, ratio]]
        df = pd.DataFrame(table, columns=self.HEADER)
        pd.options.display.max_columns = None
        # display(df)
        print df
        return uncompressed_len, compressed_len, dict_size
