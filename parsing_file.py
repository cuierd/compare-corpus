#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# University of Zurich
# Department of Computational Linguistics

# Author(s): Cui Ding
# date: 29.05.2022

# Intermediate Methods and Programming in Digital Linguistics
# Project: Corpus Comparison

# Example corpora:
# Downloaded from Gutenberg.
# Hard wrapped text file.
# 1. Pride and Prejudice, written by Jane Austen.
# 2. Politics.

# Task --> combine various modules to preprocess a single file, and get the vso-triples
# 1. preprocess a single file
# 2. get the target vso chunks for a single file
# 3. reset the class variables to save memory

from preprocessing import computer_average, Preprocessor
from paragraph_sentence_gen import generate_para
from VSO_chunks import VsoGenerator
from typing import List, Tuple


def preprocess_one_file(args_prep) -> Tuple[float, float, Tuple, Tuple, List]:
    """
    for a single file, preprocess it, getting the statistics for output
    getting the most common entities and most common verbs for output
    getting the whole sentences list and the most common verbs also for further generating vso-triples
    """
    file, max_ent, max_v = args_prep
    para = generate_para(file)
    for p in para:
        sent_obj = Preprocessor(p)
        Preprocessor.get_ner(sent_obj)
        Preprocessor.get_verb(sent_obj)
        Preprocessor.get_sum_token_sent_char(sent_obj)
    avg_word_len = computer_average(Preprocessor.char_sum, Preprocessor.token_sum)
    avg_sent_len = computer_average(Preprocessor.token_sum, Preprocessor.sent_sum)
    top_ent = Preprocessor.ner_counts.most_common(max_ent)
    top_verb = Preprocessor.verb_counts.most_common(max_v)
    assert len(Preprocessor.sentence_list) == Preprocessor.sent_sum
    return avg_word_len, avg_sent_len, top_ent, top_verb, Preprocessor.sentence_list


def get_vso_one_file(args_vso) -> List[Tuple]:
    """for a single file, get the target vso triples (most common vso triples for target verbs)."""
    sentences, top_verb, max_tr = args_vso
    target_verb = []
    for i in top_verb:
        target_verb.append(i[0])
    for sent in sentences:
        sent_obj = VsoGenerator(sent, target_verb)
        VsoGenerator.get_vso_all_text(sent_obj)
    vso_triples = VsoGenerator.vso_counts.most_common(max_tr)
    return vso_triples


def clear_up_data():
    """reset the class variables to save memory, and to avoid disturbing each other when using multiprocessing."""
    Preprocessor.reset()
    VsoGenerator.reset()
