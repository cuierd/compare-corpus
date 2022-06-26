#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# University of Zurich
# Department of Computational Linguistics

# Author(s): Cui Ding
# date: 30.05.2022

# Intermediate Methods and Programming in Digital Linguistics
# Project: Corpus Comparison

# Example corpora:
# Downloaded from Gutenberg.
# Hard wrapped text file.
# 1. Pride and Prejudice, written by Jane Austen.
# 2. Politics.

# Task --> Test preprocessing module


from unittest import TestCase, main
from preprocessing import Preprocessor


class LpTest(TestCase):
    """
    Preprocessor non-functional tests
    """
    def test_output_split_into_sentences_function(self):
        para = 'In a few days Mr. Bingley returned Mr. Bennet’s visit, and sat about ten minutes with him in his ' \
               'library. He had entertained hopes of being admitted to a sight of the young ladies, of whose beauty ' \
               'he had heard much; but he saw only the father. The ladies were somewhat more fortunate, for they had ' \
               'the advantage of ascertaining from an upper window, that he wore a blue coat and rode a black horse.'
        para_obj = Preprocessor(para)
        result = para_obj.split_into_sentences()
        self.assertIsInstance(result, list, "Required type of output is list")
        self.assertEqual(len(result), 3)
        self.assertIn('Mr. Bingley', result[0], "'Mr. Bingley' should not be split")

    def test_output_parse_token_lemma_dependency(self):
        para = 'I like apple and pear.'
        para_obj = Preprocessor(para)
        result = para_obj._parse_token_lemma_dependency()
        self.assertIsInstance(result[0], list, "Required type is list")
        self.assertEqual(result[1], 18, "There are 18 characters")

    def test_output_get_verb(self):
        para_1 = 'I like apple and pear.'
        para_2 = 'I eat apple. He drinks orange juice. We like the weather.'
        p1 = Preprocessor(para_1)
        Preprocessor.get_verb(p1)
        p2 = Preprocessor(para_2)
        Preprocessor.get_verb(p2)
        result = dict(Preprocessor.verb_counts)
        target = {'like': 2, 'eat': 1, 'drink': 1}
        self.assertEqual(result, target)
        self.assertIsInstance(result, dict, "Required type is dict")
        self.assertEqual(len(result), len(target))

    def test_output_get_sum_token_sent_char(self):
        para_1 = 'I like apple and pear.'
        para_2 = 'I eat apple. He drinks orange juice. We like the weather.'
        p1 = Preprocessor(para_1)
        p2 = Preprocessor(para_2)
        Preprocessor.get_sum_token_sent_char(p1)
        Preprocessor.get_sum_token_sent_char(p2)
        self.assertIsInstance(Preprocessor.sent_sum, int)
        self.assertEqual(Preprocessor.sent_sum, 4)
        self.assertEqual(Preprocessor.token_sum, 20)
        self.assertEqual(Preprocessor.char_sum, 65)
        

if __name__ == '__main__':
    main()
