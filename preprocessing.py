#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# University of Zurich
# Department of Computational Linguistics

# Author(s): Cui Ding
# date: 13.05.2022

# Intermediate Methods and Programming in Digital Linguistics
# Project: Corpus Comparison

# Example corpora:
# Downloaded from Gutenberg.
# Hard wrapped text file.
# 1. Pride and Prejudice, written by Jane Austen.
# 2. Politics.

# Task --> preprocess a file
# 1. split into sentences
# 2. tokenization
# 3. lemmatization
# 4. dependency parsing
# 5. named entity recognition
# 6. computer the average sentence length and word length


import spacy
from typing import List, Tuple
from collections import Counter

nlp = spacy.load("en_core_web_sm")


class Preprocessor:
    """The preprocessor class contains the paragraph and some metadata on that paragraph."""
    ner_counts = Counter()
    verb_counts = Counter()
    sentence_list = []
    sent_sum = 0
    token_sum = 0
    char_sum = 0

    def __init__(self, paragraph):
        self.paragraph = paragraph
        self.doc = nlp(self.paragraph)
        self.sentences = self.split_into_sentences()
        self.number_sent = len(self.sentences)
        self.tok_lem_dep = self._parse_token_lemma_dependency()[0]
        self.number_token = len(self.tok_lem_dep)
        self.number_char = self._parse_token_lemma_dependency()[1]

    def split_into_sentences(self) -> List:
        """Split a paragraph into a list of sentences."""
        sentences = [sent.text.strip() for sent in self.doc.sents]
        Preprocessor.sentence_list.extend(sentences)
        return sentences

    def _parse_token_lemma_dependency(self) -> Tuple:
        """get tokens, lemmas and dependency for each word in a paragraph."""
        tok_lem_dep = tuple()
        tld = []
        char_num = 0
        for token in self.doc:
            if token.text:
                tok_lem_dep = token.text, token.lemma_, token.dep_
                tld.append(tok_lem_dep)
                char_num += len(token.text)
        return tld, char_num

    @classmethod
    def get_ner(cls, self) -> Counter:
        """get the most common 15 named entities."""
        ent_lab = tuple()
        for ent in self.doc.ents:
            ent_lab = ent.text, ent.label_
            cls.ner_counts[ent_lab] += 1
        return cls.ner_counts

    @classmethod
    def get_verb(cls, self) -> Counter:
        """get the count for all the verbs."""
        for token in self.doc:
            if token.pos_ == "VERB":
                cls.verb_counts[token.lemma_] += 1
        return cls.verb_counts

    @classmethod
    def get_sum_token_sent_char(cls, self):
        """computer the sum for the number of all the sentences, tokens and characters."""
        cls.sent_sum += self.number_sent
        cls.token_sum += self.number_token
        cls.char_sum += self.number_char
        return cls.sent_sum, cls.token_sum, cls.char_sum

    @classmethod
    def reset(cls):
        """
        empty the class variables to save memory and to avoid potential interferences among different file objects
        """
        cls.ner_counts.clear()
        cls.verb_counts.clear()
        cls.sentence_list = []
        cls.sent_sum = 0
        cls.token_sum = 0
        cls.char_sum = 0


def computer_average(a, b):
    """
    a function for compute the average word number of the sentences or every character number of the words,
    given 'a' as the total number of words or characters,
    and given 'b' as the total number of sentences or words.
    """
    return round(a/b, 3)


