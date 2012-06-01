#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Annotates a text using the PALAVRAS Part of Speech Tagger.
The different levels of analysis and outputs are:
A) Dependency Trees:
    /opt/palavras/por.pl < filename
    /opt/palavras/por.pl --dep < filename
B) State of the art, noun and name semantics:
    /opt/palavras/por.pl --sem < filename
C) Morphology only (as cg cohorts):
    /opt/palavras/por.pl --morf < filename
D) Morphology plus syntax:
    /opt/palavras/por.pl --syn < filename
E) Semantic plus dependency trees:
    /opt/palavras/por.pl --sem < filename | /opt/palavras/bin/cg2dep pt
F) MALT XML output:
    /opt/palavras/por.pl < filename | /opt/palavras/bin/visldep2malt
G) MALT XML output plus name semantics:
    /opt/palavras/por.pl < filename | /opt/palavras/bin/visldep2malt | /opt/palavras/bin/extra2sem
H) Creates visl-style SOURCE and ID lines, as for input to graphical trees:
    /opt/palavras/por.pl < filename | /opt/palavras/bin/dep2tree_pt
I) TIGER XML output:
    /opt/palavras/por.pl < filename | perl -wnpe 's/^=//;' | /opt/palavras/bin/visl2tiger.pl | /opt/palavras/bin/extra2sem
"""

import subprocess
import sys
from tags_dictionary import WORD_CLASSES, INF_TAGS, SYN_TAGS, SUB_TAGS, VALENCY_TAGS
#import re

PALAVRAS_ENCODING = sys.getfilesystemencoding()
PALAVRAS_PATH = '/opt/palavras/'
base_parser = PALAVRAS_PATH + 'por.pl'
parser_mode = '--dep'
malt_parser = PALAVRAS_PATH + 'bin/visldep2malt'
tiger_parser = PALAVRAS_PATH + 'bin/visl2tiger.pl'
#regexp_tag = re.compile('<[^>]+>')

def process(text):
    process = subprocess.Popen([base_parser, parser_mode], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(text.encode(PALAVRAS_ENCODING))
    data = []
    for line in stdout.split('\n'):
        line = line.strip().decode(PALAVRAS_ENCODING)
        print line
        chunks = ''.join([chunk for chunk in line.split() if chunk.startswith('#')])
        if line.isspace() or line == '':
            data.append(['blank line'])
        elif line.startswith('<'):
            data.append(['end_sentence'])
        elif line.startswith('$'):
            non_word = line.split()[0][1:]
            if non_word.isdigit():
                non_word_type = 'number'
            else:
                non_word_type = 'punctuation'
            data.append(['non word', non_word, non_word_type, chunks])
        else:
            word = line.split('\t')[0].strip()    
            lemma = line.split('\t')[1].split()[0]
            syn_sem_tags = line.split('\t')[1].split()[1:]
            word_class = ''.join([wc for wc in syn_sem_tags if wc in WORD_CLASSES])
            secondary_tag = ' '.join([sct for sct in syn_sem_tags if sct.startswith('<')])            
            inflexion_tag = ' '.join([it for it in syn_sem_tags if it in INF_TAGS])
            syntactic_tag = ''.join([st for st in syn_sem_tags if st.startswith('@')])
            data.append([word, lemma, word_class, secondary_tag, inflexion_tag, syntactic_tag, chunks])
    return data

if __name__ == '__main__':
    txtfile = '/home/rsouza/file2.txt'
    document_text = open(txtfile,'r').read().decode(PALAVRAS_ENCODING)
    output = process(document_text)
    for line in output: print line 
#        if len(line)>4:
#            print line[0], ' ', line[4]