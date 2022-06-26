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

# Task --> Test paragraph_sentence_gen module
# 1. test generate_para
# 2. test generate_sent


from unittest import TestCase, main
from paragraph_sentence_gen import generate_para, generate_sent


class LpTest(TestCase):
    """
    test functions generate_para and generate_sent
    """

    def test_output_generate_sent(self):
        para = "In a few days Mr. Bingley returned Mr. Bennet’s visit, and sat\nabout ten minutes with him in his " \
               "library. He had entertained\nhopes of being admitted to a sight of the young ladies, of whose\n" \
               "beauty he had heard much; but he saw only the father. The ladies\nwere somewhat more fortunate, " \
               "for they had the advantage of\nascertaining from an upper window, that he wore a blue coat and\nrode " \
               "a black horse."
        result = generate_sent(para)
        self.assertIsInstance(result, object, "Required type of output is an object")
        self.assertEqual(len(list(result)), 3, "There are 3 sentences yielded")

    def test_output_generate_para(self):
        result = generate_para("data/test_text.txt")
        self.assertIsInstance(result, object, "Required type is an object")
        self.assertEqual(len(list(result)), 1, "There is one element been yielded")


if __name__ == '__main__':
    main()
