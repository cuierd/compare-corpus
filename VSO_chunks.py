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

# Task --> getting triples of the form verb-subject-object for the three most common verbs
# 1. get a sentence, generate a VSO object from this sentence
# 2. use spacy to parse sentence, get noun chunks from it
# 3. merge noun chunks to get VSO triples.
# 4. Count the most common VSO triples for the most common verbs in a text.


import spacy
from typing import List, Tuple
from collections import Counter

nlp = spacy.load("en_core_web_sm")


class VsoGenerator:
    """
    get triples of the form verb-subject-object for a number of most common verbs
    :param sentence: the sentence to parse.
    :param target_verb: a list of verbs for which we want to find the vso triples.
    """
    vso_counts = Counter()

    def __init__(self, sentence, target_verb):
        self.sentence = sentence
        self.doc = nlp(self.sentence)
        self.target_verb = target_verb
        self.chunks = self.get_noun_chunk_spacy()
        self.vso = self.merge_into_vso()

    def get_noun_chunk_spacy(self) -> List[Tuple]:
        """parse a sentence, get noun chunks out of it."""
        noun_chunk = tuple()
        chunks = []
        for chunk in self.doc.noun_chunks:
            noun = chunk.text
            dependency = chunk.root.dep_
            head = chunk.root.head.lemma_
            noun_chunk = noun, dependency, head
            chunks.append(noun_chunk)
        return chunks

    def merge_into_vso(self) -> List[Tuple]:
        """
        merge two noun chunks into one VSO-triple, if one noun chunks has the subject, the other has the object.
        in normal sentence, the subject noun chunk and the object one share the same verb.
        in passive sentence, the subject noun chunk marked by 'by' as its verb, the object marked by a normal verb.
        """
        vso = []
        vso_dict = {}
        if self.chunks:
            for noun_dep_head in self.chunks:
                # get the noun (can be subject or object)
                noun = noun_dep_head[0]
                # get the dependency
                dep = noun_dep_head[1]
                # get the verb (or 'by' etc.)
                verb = noun_dep_head[2]
                # when verb among target verb or verb is 'by', we keep it
                if verb in self.target_verb or verb == 'by':
                    # make the verb the key of the vso_dict.
                    # the value is still a dict, dep is the key of it, noun the value
                    if verb in vso_dict:
                        vso_dict[verb][dep] = noun
                    else:
                        vso_dict[verb] = {dep: noun}
            # print(vso_dict)
            # first case: the sentence is normal (not passive), e.g. 'I eat an apple.'
            vso = [(key, vso_dict[key]['nsubj'], vso_dict[key]['dobj']) for key in vso_dict if 'nsubj' in vso_dict[key]\
                   and 'dobj' in vso_dict[key]]

            # second case: the sentence is passive. e.g. 'The apple is eaten by me.'
            if 'by' in vso_dict and 'pobj' in vso_dict['by']:
                for key in vso_dict:
                    if 'nsubjpass' in vso_dict[key]:
                        vso.append((key, vso_dict['by']['pobj'], vso_dict[key]['nsubjpass']))
        return vso

    @classmethod
    def get_vso_all_text(cls, self) -> Counter:
        """
        combine all the target vso chunks from sentences to get the vso chunks and their counts for the whole text
        """
        if self.vso:
            for triple in self.vso:
                cls.vso_counts[triple] += 1
        return cls.vso_counts

    @classmethod
    def reset(cls):
        """
        empty the class variable to save memory and to avoid potential interferences among different file objects
        """
        cls.vso_counts.clear()

