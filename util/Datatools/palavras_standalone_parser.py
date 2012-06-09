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
import nltk
from tags_dictionary import WORD_CLASSES, INF_TAGS #, SYN_TAGS, SUB_TAGS, VALENCY_TAGS

PALAVRAS_ENCODING = sys.getfilesystemencoding()
PALAVRAS_PATH = '/opt/palavras/'
base_parser = PALAVRAS_PATH + 'por.pl'
parser_mode = '--dep'
malt_parser = PALAVRAS_PATH + 'bin/visldep2malt' #not used for now
tiger_parser = PALAVRAS_PATH + 'bin/visl2tiger.pl' #not used for now

def palavras_tagging(text):
    process = subprocess.Popen([base_parser, parser_mode], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(text.encode(PALAVRAS_ENCODING))
    text_and_all_tags = []
    text_and_pos_tags = []    
    for line in stdout.split('\n'):
        line = line.strip().decode(PALAVRAS_ENCODING)
        chunks = ''.join([chunk for chunk in line.split() if chunk.startswith('#')])
        if line.isspace() or line == '':
            text_and_all_tags.append(['blank line','','BL','','','',''])
        elif line.startswith('<'):
            text_and_all_tags.append(['end_sentence','','ES','','','',''])
        elif line.startswith('$'):
            non_word = line.split()[0][1:]
            if non_word.isdigit():
                non_word_type = 'number'
            else:
                non_word_type = 'punctuation'
            text_and_all_tags.append(['non word', non_word, non_word_type, '', '', '', chunks])
        elif len(line.split('\t')) < 2:  #discard malformed lines
            continue
        else:
            word = line.split('\t')[0].strip()    
            lemma = line.split('\t')[1].split()[0]
            syn_sem_tags = line.split('\t')[1].split()[1:]
            pos_tag = ''.join([wc for wc in syn_sem_tags if wc in WORD_CLASSES])
            secondary_tag = ' '.join([sct for sct in syn_sem_tags if sct.startswith('<')])            
            inflexion_tag = ' '.join([it for it in syn_sem_tags if it in INF_TAGS])
            syntactic_tag = ''.join([st for st in syn_sem_tags if st.startswith('@')])
            text_and_all_tags.append([word, lemma, pos_tag, secondary_tag, inflexion_tag, syntactic_tag, chunks])
    num_tokens = len(text_and_all_tags)
    for position in range(num_tokens):
        text_and_pos_tags.append((text_and_all_tags[position][0], text_and_all_tags[position][2]))    
    return text_and_all_tags, text_and_pos_tags #palavras style, nltk style

def np_extraction(text_and_pos_tags):
    nprules = r'''
        NP: {(<DET>+<ADJ>+<KC>+)*<ADJ|ADV|DET|NUM>*<N>+(<ADJ|ADV|DET|NUM|PRP|SPEC>*<N>+)*(<KC>+<ADJ|ADV|NUM>+)*}
            {(<DET>+<ADJ>+<KC>+)*<ADJ|ADV|DET|NUM>*<N>+<ADJ|ADV|NUM>*(<KC>+<ADJ|ADV|NUM>+)*}
            {(<DET>+<ADJ>+<KC>+)*<ADJ|ADV|DET|NUM>*<PROP>+(<ADJ|ADV|DET|NUM|PRP|SPEC>*<N>+)*(<KC>+<ADJ|ADV|NUM>+)*}
            {(<DET>+<ADJ>+<KC>+)*<ADJ|ADV|DET|NUM>*<PROP>+<ADJ|ADV|NUM>*(<KC>+<ADJ|ADV|NUM>+)*}
            '''
    chunking_parser = nltk.RegexpParser(nprules)
    chunked_tree = chunking_parser.parse(text_and_pos_tags)
    np_trees = [np.leaves() for np in chunked_tree if isinstance(np, nltk.tree.Tree) and np.node == 'NP']
    np_list = []
    for np in np_trees:
        l = [word for word, tag in np]
        np_list.append(l)
    #word, tag = zip(*noun_phrases[795])
    return np_list    


def chunks2strings(chunks):
    strings = []    
    for l in chunks:
        strings.append(' '.join(l))
    return strings


if __name__ == '__main__':
    txtfile = '/home/rsouza/3110202.txt'#file.txt'    
    document_text = open(txtfile,'r').read().decode(PALAVRAS_ENCODING)
    parsed_text = palavras_tagging(document_text)
    noun_phrases = np_extraction(parsed_text[1])
    noun_phrases = chunks2strings(noun_phrases)
    for np in noun_phrases: 
        print np
    fd = nltk.FreqDist(word.lower() for word in noun_phrases)
    fd.plot(30)
