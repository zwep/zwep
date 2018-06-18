# -*- coding: utf-8 -*-

"""
This contains some word embedding tactic classes

"""


import collections
import itertools
import warnings
import numpy as np

from dia.helper.miscfunction import cluster_diff_list


class TFIDF:
    """
    Making TFIDF possible via my own class. Reason being, the TfidfVectorizer from sklearn
    was (IMO) too complex and did not (clearly) offer any variation on the tf and idf.

    No preprocessing is done here, you can do this yourself. That is so much clearer (IMO).
    PLEASEPLEASEPLEASE
    CHECK/TEST if the dictionary is keeping good reference to the actualy places...
    Because dictionaries can order their keys sometimes alphabetically, and sometimes not.
    Sometimes this is desired and sometimes not...

    """
    def __init__(self, document_list):
        """
        :param document_list: list of sentences, can also be seen as a list of strings.
        """
        if all([isinstance(x, list) for x in document_list]):
            self._type = 'list'
        elif all([isinstance(x, str) for x in document_list]):
            self._type = 'str'
        else:
            warnings.warn('We might have mixed types in the given list')

        self.document_list = document_list
        if self._type == 'str':
            unique_words = list(set(itertools.chain(*[x.split() for x in self.document_list])))
        elif self._type == 'list':
            unique_words = list(set(itertools.chain(*self.document_list)))

        self.vocab_dict_num = dict(enumerate(unique_words))
        self.vocab_dict = {v: k for k, v in self.vocab_dict_num.items()}

        self.word_N = len(unique_words)
        self.idf_N = len(self.document_list)
        self._tf()
        self._idf()

        # A start to asses whether the assingmet went okay
        # Still kinda rubish. But with helper.miscfunction.compare_dict() this gives some nice results.
        z = np.nonzero(self.TF_count)
        w = cluster_diff_list(z[0], list(map(self.vocab_dict_num.get, z[1])))
        val = cluster_diff_list(z[0], [x for x in self.TF_count.ravel() if x > 0])
        self.test = [dict(zip(k, v)) for k, v in zip(w, val)]
        self.testidfweight = {self.vocab_dict_num[i]: x for i, x in enumerate(self.IDF_weight)}
        self.testidf = {self.vocab_dict_num[i]: x for i, x in enumerate(self.IDF)}

    def _tf(self):
        """
        Initializes the Term Frequency for the given documents.
        All variations are dependent on this one, as well as the IDF.
        Output is the (#documents x # words in vocab)
        """
        self.TF_count = np.zeros(shape=(self.idf_N, self.word_N))
        for i_index, x in enumerate(self.document_list):
            # import nltk
            # words = nltk.tokenize.word_tokenize(x)
            if self._type == 'str':
                words = x.split()
            elif self._type == 'list':
                words = x
            word_counter_obj = collections.Counter(words)
            # Get the mapping from the unique words of this document to the full document vocabulary indices
            position_value = list(map(self.vocab_dict.get, word_counter_obj.keys()))
            # And map the values of the counts (using position_vlaue) to the TF_count object.
            self.TF_count[i_index, position_value] = list(word_counter_obj.values())

        return self.TF_count

    def tf_bin(self):
        """
        The binary version of the Term Frequency
        """
        return (self.TF_count != 0).astype(int)

    def tf_freq(self):
        """
        The scaled version of the Term Frequency
        """
        ftd_len = self.TF_count.sum(axis=1)
        freq = self.TF_count / ftd_len[:, None]
        return freq

    def tf_log_freq(self):
        """
        The log version of the Term Frequency
        """
        log_freq = 1 + np.log(np.ma.log(self.TF_count)).filled(0)
        return log_freq

    def tf_augmented_freq(self):
        """
        The augmented freuqency version of the Term Frequency
        """
        ftd_max = self.TF_count.max(axis=1)
        augmented_freq = 0.5 + 0.5 * self.TF_count / ftd_max[:, None]
        return augmented_freq

    def _idf(self):
        """
        The Inverse Document Frequency. All IDFs outputs a vector the size of the vocab.
        """

        tf_count_non_zero = np.array([x.astype(bool).astype(int) for x in self.TF_count])
        self.IDF_weight = np.sum(tf_count_non_zero, axis=0)
        self.IDF = np.log(self.idf_N/(1+self.IDF_weight))
        return self.IDF

    def idf_smooth(self):
        """
        The smoothed version of the Inverse Document Frequency
        """
        smooth = np.log(1 + self.idf_N/self.IDF_weight)
        return smooth

    def idf_max(self):
        """
        The max version of the Inverse Document Frequency
        """
        max_value = np.log(max(self.IDF_weight)/(1+self.IDF_weight))
        return max_value

    def idf_prob(self):
        """
        The probabilistic version of the Inverse Document Frequency
        """
        prob = np.log((self.idf_N - self.IDF_weight)/self.IDF_weight)
        return prob
