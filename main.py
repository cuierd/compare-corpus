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
# 1. Make command line interface,
# 2. which can take two files as input files and parse them.
# 3. print the metadata into command line or into a html file.

import sys
from parsing_file import preprocess_one_file, get_vso_one_file, clear_up_data
from argparse import ArgumentParser
import time
from typing import List, TextIO, Tuple
from multiprocessing import Pool


IN_FILE_1 = 'data/PrideAndPrejudice.txt'
IN_FILE_2 = 'data/Politics.txt'


def get_cli() -> ArgumentParser:
    """Command line interface that allows the user to compare text files and print the metadata."""
    parser = ArgumentParser("VSO", description="Parse given files, get metadata and VSO triples.")
    parser.add_argument('--file_1', '-f1', default=IN_FILE_1, metavar='FILE', type=str,
                        help="The two files to be compared.")
    parser.add_argument('--file_2', '-f2', default=IN_FILE_2, metavar='FILE', type=str,
                        help="The two files to be compared.")
    parser.add_argument('--print', '-p', action='store_true', help="Print the metadata and VSO triples to command line.")
    parser.add_argument('--max_ent', '-e', type=int, default=15,
                        help="The number of the most common named entity to be printed.")
    parser.add_argument('--max_verb', '-v', type=int, default=3,
                        help="The number of the most common verbs to be used to generate VSO.")
    parser.add_argument('--max_triple', '-t', type=int, default=15,
                        help="The number of the most common VSO triples to be printed.")
    parser.add_argument('--output_file', '-o', type=str, default=sys.stdout, metavar='FILE',
                        help="Write the metadata of comparing two text files out.")
    return parser


def pretty_print(w_len: float, s_len: float, top_e: Tuple, top_v: Tuple, vso_triple: List[Tuple]) -> None:
    """
    Print the outputs of comparing two files into the screen, with data for average word length, average sentence
    length, most common named entities, most common verbs, most common vso chunks.
    """
    print(f"Average word length: {w_len}")
    print(f"Average sentence length: {s_len}")
    print("-" * 40)
    print(f"Most common {len(top_e)} named entities: ")
    for key, value in top_e:
        print(key, "-->", value)
    print("-" * 40)
    print(f"Most common {len(top_v)} verbs: ")
    for key, value in top_v:
        print(key, "-->", value)
    print("-" * 40)
    print(f"Most common {len(vso_triple)} VSO triples: ")
    for key, value in vso_triple:
        print(key, "-->", value)
    clear_up_data()
    print()


def write_html_body(args_html: Tuple) -> None:
    """
    Write the comparison of two files into html table.
    Data for one file stays in one row.
    Data includes average word length, average sentence length, most common named entities, most common verbs,
    most common vso chunks
    """
    file, outfile, w_len, s_len, top_e, top_v, vso_triple = args_html
    with open(outfile, 'a', encoding='utf-8') as otf:
        otf.write('     <tr> ')
        filename = file.split('/')[1][:-4]
        otf.write(f'<td>{filename}</td>')
        otf.write(f'<td>{w_len}</td>')
        otf.write(f'<td>{s_len}</td>')
        otf.write('<td>')
        for key, value in top_e:
            otf.write(f'{key} --> {value}<br />')
        otf.write('</td>')
        otf.write('<td>')
        for key, value in top_v:
            otf.write(f'{key} --> {value}<br />')
        otf.write('</td>')
        otf.write('<td>')
        for key, value in vso_triple:
            otf.write(f'{key} --> {value}<br />')
        otf.write('</td>')
        otf.write('\n')
        otf.write('     </tr>')
        clear_up_data()


def write_html_head(files: List, max_e: int, max_v: int, max_tr: int, otf: TextIO) -> None:
    """
    Write the head and title etc. for the html file and the table in it.
    """
    f1 = files[0].split('/')[1][:-4]
    f2 = files[1].split('/')[1][:-4]
    otf.write('<html>')
    otf.write(f' <head><title>Compare Corpora: {f1} VS. {f2}</title></head>')
    otf.write(' <body>')
    otf.write(f'  <h1>Compare Corpora: {f1} VS. {f2}</h1>')
    otf.write(f'  <h2>Only {max_tr} examples are presented for VSO triples! Otherwise it is too full.</h2>')
    otf.write('  <table border = "5">')
    otf.write(f'<tr><th>book</th><th>avg_word_len</th><th>avg_sent_len</th><th>top{max_e}_ent</th><th>top{max_v}_verb</th><th>\
    top{max_tr}_VSO_triples</th></tr>')


def write_html_end(otf: TextIO) -> None:
    """
    Write the ending for the html table.
    """
    otf.write('  </table>')
    otf.write(' </body>')
    otf.write('</html>')


def main():
    parser = get_cli()
    args = parser.parse_args()
    files = [args.file_1, args.file_2]
    # for multiprocessing. Better to use starmap which is more professional.
    # I choose to use this naive way to pass multiple arguments to a function once.
    # The first argument will change according to files. The second and third stay the same.
    args_tuple = [(args.file_1, args.max_ent, args.max_verb), (args.file_2, args.max_ent, args.max_verb)]

    t1 = time.time()

    # If we need to print to the screen
    if args.output_file == sys.stdout or args.print:
        print("* I am working hard ... Be patient please :-) *")
        # Use multiprocessing, parse two files together
        with Pool() as pool:
            # Call on the function 'preprocess_one_file'. Pass the arguments tuple. Deal with two files.
            rt = pool.map(preprocess_one_file, args_tuple)
            # Get the first stage results. Pick the ones we will use as arguments for next function. Make them a tuple.
            args_vso = [(rt[0][4], rt[0][3], args.max_triple), (rt[1][4], rt[1][3], args.max_triple)]
            # Call on the function 'get_vso_one_file'. Pass the argument tuple from above. Deal with two files.
            vso_rt = pool.map(get_vso_one_file, args_vso)

            # For the two files, print the results.
            print("** Working on : ", args.file_1.split('/')[1], "**")
            pretty_print(rt[0][0], rt[0][1], rt[0][2], rt[0][3], vso_rt[0])
            print("** Working on : ", args.file_2.split('/')[1], "**")
            pretty_print(rt[1][0], rt[1][1], rt[1][2], rt[1][3], vso_rt[1])

    # If we need to write to a html file to store the results in a table
    if args.output_file != sys.stdout:
        # write the head
        with open(args.output_file, 'w', encoding='utf-8') as otf:
            write_html_head(files, args.max_ent, args.max_verb, args.max_triple, otf)
        # Parse the two files as in last part, using multiprocessing.
        # Write the results to the body of the html table, also using multiprocessing to write faster.
        with Pool() as pool:
            rt = pool.map(preprocess_one_file, args_tuple)
            args_vso = [(rt[0][4], rt[0][3], args.max_triple), (rt[1][4], rt[1][3], args.max_triple)]
            vso_rt = pool.map(get_vso_one_file, args_vso)
            args_html = [(args.file_1, args.output_file, rt[0][0], rt[0][1], rt[0][2], rt[0][3], vso_rt[0]),
                         (args.file_2, args.output_file, rt[1][0], rt[1][1], rt[1][2], rt[1][3], vso_rt[1])]
            pool.map(write_html_body, args_html)
        # Write the ending of the html file/table.
        with open(args.output_file, 'a', encoding='utf-8') as otf:
            write_html_end(otf)

    t2 = time.time()
    print("time:", t2-t1)


if __name__ == "__main__":
    main()
