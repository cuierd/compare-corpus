# Semester Project: Compare two Corpora

## Intermediate Methods and Programming in Digital Linguistics

**Cui Ding (olatname: cding)**

## Introduction

**1. Goal**:
* This is a project to compare two corpora, e.g. hard wrapped text file downloaded from Gutenberg.

**2. Steps**:

**2.1 Generate paragraphs out of the hard wrapped text file.**
  * ```paragraph_sentence_gen.py``` --> function: ```generate_para```
    * Text file with soft line wrap can also be compared with just a tweak in the codes. --> function: ```generate_sent```
    
**2.2 Preprocess text file**
* Create class ```Preprocessor``` and use SpaCy to do --> ```preprocessing.py```:
  * tokenization 
  * lemmatization
  * dependency parsing
  * named entity recognition(NER)
  * collect the verbs
  * get the total number of sentences, words, characters
* A function to calculate the average
  * average sentence length
  * average word length
* Store the results to use later

**2.3 Collect VSO triples**
* Create class ```VsoGenerator``` and use SpaCy to do --> ```VSO_chunks.py```:
  * noun chunk parsing
    * For the simple sentence “I ate an apple”, the spaCy chunker output is:
    
       &nbsp; &nbsp; &nbsp; I &nbsp; &nbsp; &nbsp;nsubj &nbsp; &nbsp; &nbsp;ate
    
      &nbsp; &nbsp; &nbsp; an apple &nbsp; &nbsp; &nbsp; dobj &nbsp; &nbsp; &nbsp; ate
    
      The resulting triple should be: (‘eat’, ‘I’, ‘apple’)
    
    * Also works for complex sentences with multiple verbs. For example, for the sentence: "Paul Lesutis, who manages the investments at Provident Capital Management Inc., blames futures markets." the spaCy chunker output is:
      
      &nbsp; &nbsp; &nbsp; Paul Lesutis &nbsp; &nbsp; &nbsp; nsubj &nbsp; &nbsp; &nbsp; blames
    
      &nbsp; &nbsp; &nbsp; who &nbsp; &nbsp; &nbsp; nsubj &nbsp; &nbsp; &nbsp; manages
    
      &nbsp; &nbsp; &nbsp; the investments &nbsp; &nbsp; &nbsp; dobj &nbsp; &nbsp; &nbsp; manages
  
      &nbsp; &nbsp; &nbsp; Provident Capital Management Inc. &nbsp; &nbsp; &nbsp; pobj &nbsp; &nbsp; &nbsp; at
  
      &nbsp; &nbsp; &nbsp; futures markets &nbsp; &nbsp; &nbsp; dobj &nbsp; &nbsp; &nbsp; blames
      
      The resulting triples should be: (‘blame’, ‘Paul Lesutis’, ‘futures markets’) and (‘manage’, ‘who’, ‘the investments’)
    * Works for passive sentences, where the subject marked by spaCy as “nsubjpass” should end up in the object position of the triple, and the prepositional object “pobj” with “by” should occupy the subject position in the triple.
      
      For example, "The books were given to him by Peter.” should lead to the triple (‘give’, ‘Peter’, ‘The books’)
    
  * merge noun chunks into VSO chunks for target verbs
  * store target VSO chunks across the whole text
  
**2.4 Combine 2.1, 2.2, 2.3 and parse for one file**
* get statistics 
* get most common entities, verbs for parameters which are passed by command line.
* ```parsing_file.py```

**2.5 Command line interface**

* One can set the parameters more freely by CLI. --> ```main.py``` function: ```get_cli()```
  * The two files one wants to compare.
  * The number of most common named entities.
  * The number of most common verbs one wants to see and to use to generate VSO triples.
  * The number of most common VSO to be output.
  * The output format:
    * pretty print to the screen
    * write to an HTML table



> **NOTE:<br>1. It takes about 58s to run it once with multiprocessing (for the default parameters).<br>2. Without multiprocessing, it takes about 88s to run.<br>**


## Details

Examples for how the CLI could work:

* Print to command line, parameters are default values:
  * The first file to be compared (--file_1 or -f1): data/PrideAndPrejudice.txt
  * The second file to be compared (--file_2 or -f2): data/Politics.txt
  * The maximum most common named entities to be printed/ write out (--max_ent or -e): 15
  * The maximum most common verbs to be printed/ write out (--max_verb or -v): 3
  * The maximum most common VSO triples to be printed/ write out (--max_triple or -t): 15
  * The output format (--print or -p): print to screen

```sh
$ python3 main.py 
$ python3 main.py -p
```

* Write out to a html file, called *my_comparison.html*. 
  * parameters are default values as above except for the --print/-p statement:

```sh
$ python3 main.py -o my_comparison.html
```

* Set other parameters and print to screen:
  * The first file to be compared (--file_1 or -f1): data/NYT_MonthlyMagazine1918.txt
  * The second file to be compared (--file_2 or -f2): data/Russell_ProblemsOfPhilosophy.txt
  * The maximum most common named entities to be printed/ write out (--max_ent or -e): 10 or any other positive integer
  * The maximum most common verbs to be printed/ write out (--max_verb or -v): 4 or any other positive integer
  * The maximum most common VSO triples to be printed/ write out (--max_triple or -t): 10 or any other positive integer
```sh
$ python3 main.py -e 12 -v 3 -t 20 
$ python3 main.py -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt
$ python3 main.py -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt -v 5 -t 20
$ python3 main.py -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt -e 10 -v 4 -t 10 
$ python3 main.py -p -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt -e 20 -v 3 -t 15 
```

* Set other parameters and write out as html file:
```sh
$ python3 main.py -e 12 -v 3 -t 20 -o my_comparison.html
$ python3 main.py -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt -o my_comparison.html
$ python3 main.py -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt -v 5 -t 20 -o my_comparison.html
$ python3 main.py -f1 data/NYT_MonthlyMagazine1918.txt -f2 data/Russell_ProblemsOfPhilosophy.txt -e 12 -v 3 -t 20 -o my_comparison.html
```

## Unit Test

Three Unit Test files are included: 
* ```test_paragraph_sentence_gen.py``` for testing paragraph generation and sentence generation.
* ```test_preprocessing.py``` for testing the functionality of class ```Preprocessor```.
* ```test_VSO_chunks.py``` for testing the functionality of class ```VsoGenerator```, whether it can deal with the special cases correctly.

## Multiprocessing

In ```main.py```, multiprocessing was used to improve the time efficiency. Reasons:
* Our files are in large size.
* We currently compare two files, but more files can be compared at the same time with a small adaption in the ```get_cli``` function and the ```main``` function.

## Generator and reset

Paragraphs/sentences are created by a generator to save the memory.
Class ```Preprocessor``` and ```VsoGenerator``` have ```reset``` methods for clearing up the class variables after done with one file in order to save memories. 








