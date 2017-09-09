import collections
import sys
import os
import math
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from IPython.display import display
import random
import itertools

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../huffman')))
import Huffman


class ClusteredHuffman(object):
    def __init__(self, **kwargs):
        """
        params:
          sample_seperator: which event represent seperator between samples,
                            if None, works in character level (for one liner data-sets such our reformatted json)
          batch_size: how many samples grouped to represent freq sample to the clustring algorithm
          stop_chars: chars to ignore/skip
        """
        self.sample_seperator = kwargs['sample_seperator'] if 'sample_seperator' in kwargs else None
        self.train_batch_size = kwargs['train_batch_size'] if 'train_batch_size' in kwargs else 100
        assert self.train_batch_size > 0
        self.stop_chars = kwargs['stop_chars'] if 'stop_chars' in kwargs else []
        self.n_clusters = kwargs['n_clusters'] if 'n_clusters' in kwargs else 8
        self.fill_missing_chars = kwargs['fill_missing_chars'] if 'fill_missing_chars' in kwargs else True
        self.data_set_is_file_path = kwargs['data_set_is_file_path'] if 'data_set_is_file_path' in kwargs else True
        self.verbose = kwargs['verbose'] if 'verbose' in kwargs else True
        self.train_fraction = kwargs['train_fraction'] if 'train_fraction' in kwargs else None

        self.est = None
        self.full_char_set = None
        self.h_arr = None
        self.train_labels_count = None
        self.cluster_bits_rep = math.ceil(math.log(self.n_clusters, 2))

    def info(self, msg):
        if self.verbose is True:
            print msg

    def encode(self, data_set_file, batch_size):
        self.info('encode dataset...')

        # TODO: add dictionaries to the enccoding... (for the analysis we use compression_info_file)
        # for h in self.h_arr:
        #    huff_dicts += h.get_dict_size()

        cluster_bits = '{:0%sb}' % self.n_clusters
        encode_stream = ''
        for f, curr_chars in self._get_sample(self.get_data_stream(data_set_file), batch_size, True):
            label = int(self.est.predict(f.reshape(1, -1)))
            encode_stream += cluster_bits.format(label)
            encode_stream += self.h_arr[label].encode(curr_chars)

        self.info('done encoding!')
        return encode_stream

    def get_data_stream(self, data_set_file):
        if self.data_set_is_file_path:
            return itertools.chain.from_iterable(open(data_set_file))
        return data_set_file

    def get_dicts_size(self):
        huff_dicts = 0.
        for h in self.h_arr:
            huff_dicts += h.get_dict_size()
        return huff_dicts

    def compression_info_file(self, data_set_file, batch_size):
        self.info('calculate compression info...')
        uncompressed = 0
        compressed = 0
        huff_dicts = 0.
        for f, curr_chars in self._get_sample(self.get_data_stream(data_set_file), batch_size, True):
            label = int(self.est.predict(f.reshape(1, -1)))
            curr_uncomp, curr_comp, dict_size = self.h_arr[label].compression_info(curr_chars)
            uncompressed += curr_uncomp
            compressed += curr_comp + self.cluster_bits_rep
        huff_dicts = self.get_dicts_size()
        return compressed, uncompressed, huff_dicts

    def print_compression_info_file(self, data_set_file, batch_size):
        compressed, uncompressed, huff_dicts = self.compression_info_file(data_set_file, batch_size)
        header = ['uncompressed[b]', 'compressed[b]', 'dictionaries[b]', 'neto compression ratio', 'compression ratio']
        table = [
            [uncompressed, compressed, huff_dicts, compressed / uncompressed, (compressed + huff_dicts) / uncompressed]]
        #         print 'uncompressed: %s, compressed(without codes): %s, codes: %s, ratio(without codes): %s, total ratio: %s' %(uncompressed, compressed, huff_dicts, compressed / uncompressed, (compressed + huff_dicts) / uncompressed)
        print_table(header, table)
        return compressed, uncompressed, huff_dicts

    def get_huffman_dicts_lengths(self):
        table = []
        table.append(self.full_char_set[:])
        for h in self.h_arr:
            c_len = [str(len(h.get_code()[c])) for c in self.full_char_set]
            table.append(c_len)
        return table

    def print_huffman_dicts_lengths(self):
        table = self.get_huffman_dicts_lengths()
        for row in table:
            print '%s' % (' '.join(row))

    def pprint_huffman_dicts_lengths(self):
        table = self.get_huffman_dicts_lengths()
        headers = table.pop(0)
        print_table(headers, table)

    def pprint_train_labels_count(self):
        headers = [i for i in range(len(self.train_labels_count))]
        print_table(headers, [self.train_labels_count])

    def build_codes(self, data_set_file):
        self.info('calculate full char set...')
        self.full_char_set = self._get_char_set(self.get_data_stream(data_set_file))
        self.info('build clustring samples...')
        cluster_samples = self._get_cluster_samples(self.get_data_stream(data_set_file), self.train_batch_size)
        if self.train_fraction is not None:
            self.info('#full sample size %s' % len(cluster_samples))
            cluster_samples = random.sample(cluster_samples, int(self.train_fraction * len(cluster_samples)))
        self.info('#samples: %s' % len(cluster_samples))
        self.info('clustring samples...')
        est = KMeans(n_clusters=self.n_clusters)
        self.est = est
        est.fit(cluster_samples)
        h_arr = []
        np.set_printoptions(precision=2)
        for i, c in enumerate(est.cluster_centers_):
            #             print 'centroid %s: %s' % (i, c)
            freq_dict = {self.full_char_set[i]: c[i] for i in range(len(self.full_char_set))}
            h = Huffman.Huffman(self.stop_chars)
            h.generate_code_from_freq_dict(freq_dict)
            h_arr.append(h)
        self.h_arr = h_arr
        self.info('huffman dicts code length comparrison:')
        if self.verbose:
            self.pprint_huffman_dicts_lengths()

        labels = est.predict(cluster_samples)
        self.train_labels_count = []
        for i in range(self.n_clusters):
            self.train_labels_count.append(len([l for l in labels if l == i]))
        # print 'labels_count: %s' % self.train_labels_count
        if self.verbose:
            self.pprint_train_labels_count()

    def get_train_labels_count(self):
        return self.train_labels_count

    def _get_cluster_samples(self, char_stream, batch_size):
        samples = []
        for f, _ in self._get_sample(char_stream, self.train_batch_size, False):
            samples.append(f)
        return samples

    def _get_sample(self, char_stream, batch_size, get_reminder):
        count = 0
        curr_batch = []
        for c in char_stream:
            if c in self.stop_chars:
                continue
            curr_batch.append(c)
            if c == self.sample_seperator or self.sample_seperator is None:
                count += 1
            if count == batch_size:
                freq_vec = self._get_freq(curr_batch)
                yield freq_vec, curr_batch
                count = 0
                curr_batch = []

        if get_reminder:
            if len(curr_batch) > 0:
                self.info('_get_sample fetched last partial sample length %s chars' % len(curr_batch))
                yield self._get_freq(curr_batch), curr_batch
                count = 0
                curr_batch = []
        else:
            if len(curr_batch):
                self.info('_get_sample drop last remainder sample length %s chars' % len(curr_batch))

    def _get_freq(self, char_stream):
        assert self.full_char_set is not None

        count_dict = dict(collections.Counter(char_stream))
        for c in self.stop_chars:
            if c in count_dict:
                del count_dict[c]
        char_set = set([c for c in count_dict.keys()])
        if char_set != set(self.full_char_set):
            if self.fill_missing_chars:
                for c in self.full_char_set:
                    if c not in count_dict:
                        #                         print 'fill missing char %s in sample' % c
                        count_dict[c] = 0
            else:
                raise ValueError(
                    'need to support missing chars (maybe add some constant epsilon freq for those missings)')
        total = float(sum([v for v in count_dict.values()]))
        return np.array([count_dict[k] / total for k in self.full_char_set])

    def _get_char_set(self, char_stream):
        char_set = set()
        for c in char_stream:
            if c not in self.stop_chars:
                char_set.add(c)
        return list(char_set)

def print_table(header, table):
    df = pd.DataFrame(table, columns=header)
    pd.options.display.max_columns = None
    print df
