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

# Task --> Generate paragraph and sentence out of a hard wrapped text file.
# 1. generate paragraph
# 2. generate sentence

import spacy

nlp = spacy.load("en_core_web_sm")


def generate_para(file):
    """paragraph generator"""
    with open(file, "r", encoding='utf-8') as infile:
        paragraph = ''
        for line in infile:
            if not line.isspace():
                paragraph += line.strip()
            else:
                if paragraph:
                    yield paragraph
                    paragraph = ''


def generate_sent(para):
    """sentence generator"""
    doc = nlp(para)
    for sent in doc.sents:
        yield sent.text.strip()
