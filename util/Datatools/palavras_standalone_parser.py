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
import os
import glob
import time
from tags_dictionary import WORD_CLASSES, INF_TAGS #, SYN_TAGS, SUB_TAGS, VALENCY_TAGS
 
PALAVRAS_ENCODING = sys.getfilesystemencoding()
PALAVRAS_PATH = '/opt/palavras/'
FILES_PATH = '/home/rsouza/'
base_parser = PALAVRAS_PATH + 'por.pl'
parser_mode = '--dep'
malt_parser = PALAVRAS_PATH + 'bin/visldep2malt' #Not used for now
tiger_parser = PALAVRAS_PATH + 'bin/visl2tiger.pl' #Not used for now


def files_finder(path=FILES_PATH):
    files = []
    print('\n__________________________________________\n')    
    print('Preparing the set of files to process...\n')    
    for infile in glob.glob(os.path.join(path, '*.txt') ):
        print('Reading file:\t{0}'.format(infile))
        files.append(infile)
    return files


def palavras_tagger(text):
    t0 = time.time()
    print('Sending to Palavras parser...\n')            
    process = subprocess.Popen([base_parser, parser_mode], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(text.encode(PALAVRAS_ENCODING))
    print('Processing Palavras output...\n')            
    text_and_all_tags = []
    text_and_pos_tags = []
    count = 0    
    for line in stdout.split('\n'):
        count += 1
        if count%1000 == 0:
            print('Processing token:\t{0}'.format(count))        
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
        elif len(line.split('\t')) < 2:  #Discard malformed lines
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
    t1 = time.time() - t0
    print('\n{0} tokens processed in {1:.2f} seconds ({2:.1f} tokens/second)\n'.format(count,t1,(count//t1)))
    return text_and_all_tags, text_and_pos_tags #palavras style, nltk style


def np_extractor(text_and_pos_tags):
    # These rules may be fine tuned to catch smallers or bigger NPs    
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
    return np_list    


def chunks2strings(chunks):
    strings = []    
    for l in chunks:
        strings.append(' '.join(l))
    return strings


if __name__ == '__main__':
    txt_files_in_dir = files_finder()
    for txt_file in txt_files_in_dir:
        print('____________________________________________\n')
        print('Processing file:\t{0}\n'.format(txt_file))
        document_text = open(txt_file,'r').read().decode(PALAVRAS_ENCODING)
        parsed_text = palavras_tagger(document_text)
        noun_phrases = np_extractor(parsed_text[1])
        noun_phrases = chunks2strings(noun_phrases)
        noun_phrases = [np for np in noun_phrases if len(np)>1] #Filtering single letters
        print('Saving NPs to file:\t{0}_np.out'.format(txt_file))        
        f = open('{0}_np.out'.format(txt_file), 'w')
        f.write('\n *** Noun Phrases on file:\t{0} *** \n\n'.format(txt_file))
        for np in noun_phrases: 
            #print(np)
            f.write('\n%s' % np)
        f.write('\n\n *** NP Frequencies on file:\t{0} ***\n\n'.format(txt_file))
        fd = nltk.FreqDist(word.lower() for word in noun_phrases)
        for np, freq in fd.items():
            f.write('\nNP:\t{0}\t{1}'.format(np,freq))
        #fd.plot(30)
        f.close()
        print('\nClosing file:\t{0}_np.out\n'.format(txt_file))     
        
        