#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re
import sys


PALAVRAS_ENCODING = sys.getfilesystemencoding()
PALAVRAS_PATH = '/opt/palavras/'
regexp_tag = re.compile('<[^>]+>')

def process(text):
    """Annotate a text using the PALAVRAS Part of Speech Tagger"""
    base_parser = PALAVRAS_PATH + 'por.pl'
    process = Popen([base_parser, '--morf'], stdin=PIPE, stdout=PIPE,
                    stderr=PIPE)
    stdout, stderr = process.communicate(text.encode(PALAVRAS_ENCODING))
    data = []
    for line in stdout.split('\n'):
        if not line.startswith(' '):
            token = line.strip()[2:-2]
        else:
            data.append((token.decode(PALAVRAS_ENCODING),
                         get_syntatic_category(line.strip())))
    return data

def get_syntatic_category(message):
    for word in regexp_tag.sub('', message).split():
        if not word.startswith('"'):
            return word
    raise ValueError('Bad message')

def test_split_analysis():
    assert get_syntatic_category(' "a" b') == 'b'
    assert get_syntatic_category(' "a" b c') == 'b'
    assert get_syntatic_category(' "a" <*> b c') == 'b'
    assert get_syntatic_category(' "a" <q w c s> b c') == 'b'

if __name__ == '__main__':
    test_split_analysis()
    txtfile = '/home/rsouza/file.txt'
    document_text = open(txtfile).read().decode(PALAVRAS_ENCODING)
    print process(document_text)