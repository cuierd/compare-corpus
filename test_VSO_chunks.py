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

# Task --> Test VSO_chunks module


from unittest import TestCase, main
from VSO_chunks import VsoGenerator


class LpTest(TestCase):
    """
    VsoGenerator non-functional tests
    """

    def test_output_get_noun_chunk_spacy(self):
        sent = 'I like apple and pear.'
        sent_obj = VsoGenerator(sent, "like")
        result = sent_obj.get_noun_chunk_spacy()
        target = [('I', 'nsubj', 'like'), ('apple', 'dobj', 'like'), ('pear', 'conj', 'apple')]
        self.assertIsInstance(result, list, "Required type of output is list")
        self.assertEqual(len(result), 3)
        self.assertEqual(result, target)

    def test_output_merge_into_vso(self):
        sent_1 = 'I like apple and pear.'
        s_1 = VsoGenerator(sent_1, ["like"])
        result_1 = s_1.merge_into_vso()
        target_1 = [('like', 'I', 'apple')]

        # special case: passive sentence
        sent_2 = "The cake is made by my mother."
        s_2 = VsoGenerator(sent_2, ["make"])
        result_2 = s_2.merge_into_vso()
        target_2 = [('make', 'my mother', 'The cake')]

        # special case: complex sentence
        sent_3 = "Paul Lesutis, who manages the investments at Provident Capital Management Inc., blames" \
                 " futures markets."
        s_3 = VsoGenerator(sent_3, ["manage", "blame"])
        result_3 = s_3.merge_into_vso()
        target_3 = [('blame', 'Paul Lesutis', 'futures markets'), ('manage', 'who', 'the investments')]

        self.assertIsInstance(result_1, list, "Required type is list")
        self.assertEqual(result_1, target_1, "The target is a tuple with 3 elements, a verb, a subject, an object")
        self.assertEqual(result_2, target_2, "The target is a tuple with 3 elements, a verb, a subject, an object")
        self.assertEqual(result_3, target_3, "The target is a tuple with 3 elements, a verb, a subject, an object")

    def test_output_get_vso_all_text(self):
        sent_1 = 'I like apple and pear.'
        s_1 = VsoGenerator(sent_1, "like")
        VsoGenerator.get_vso_all_text(s_1)
        sent_2 = "The cake is made by my mother."
        s_2 = VsoGenerator(sent_2, "make")
        VsoGenerator.get_vso_all_text(s_2)

        self.assertIn(('like', 'I', 'apple'), dict(VsoGenerator.vso_counts))
        self.assertIsInstance(VsoGenerator.vso_counts, object, "Required type is a Counter objects")
        self.assertEqual(len(VsoGenerator.vso_counts), 2)

    def test_output_reset(self):
        sent_1 = 'I like apple and pear.'
        s_1 = VsoGenerator(sent_1, "like")
        VsoGenerator.get_vso_all_text(s_1)
        sent_2 = "The cake is made by my mother."
        s_2 = VsoGenerator(sent_2, "make")
        VsoGenerator.get_vso_all_text(s_2)
        VsoGenerator.reset()
        self.assertEqual(len(VsoGenerator.vso_counts), 0)


if __name__ == '__main__':
    main()
