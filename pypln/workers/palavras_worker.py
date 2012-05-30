#-*- coding:utf-8 -*-
"""
Palavras parser worker
"""

import subprocess
import zmq
import re
import sys
from nltk.tag import tuple2str
from base import PushPullWorker
from zmq import ZMQError

PALAVRAS_ENCODING = sys.getfilesystemencoding()
PALAVRAS_PATH = '/opt/palavras/'


context = zmq.Context()

class PalavrasPOSTaggerWorker(PushPullWorker):
    """
    Worker to tag words in texts according to their morphological type
    Annotate a portuguese text using the PALAVRAS Part of Speech Tagger
    Expects to receive a JSON message with the following structure
    {"text":"...","lang":"<language iso code>"} where text is a raw text string.
    To be used together with the MongoUpdateSink class.
    """

    def process(self,msg):
        """Does the Portuguese POS tagging"""
        base_parser = PALAVRAS_PATH + 'por.pl'
        regexp_tag = re.compile('<[^>]+>')
        if msg['lang'] != 'pt':
            raise ValueError('Text is not in Portuguese')
        try:
            process = subprocess.Popen([base_parser, '--morf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(msg['text'].encode(PALAVRAS_ENCODING))
            tagged = []
            for line in stdout.split('\n'):
                if not line.startswith(' '): #The token itself in Palavras output
                    token = line.strip()[2:-2]
                else:                        #All Morfological data. Only "Word Class" (Syntactic) will be used
                    morf_data = line.strip()
                    for word in regexp_tag.sub('', morf_data).split():
                        if not word.startswith('"'): # The first word conforming the pattern is Word Class
                            syntactic_category = word
                            break
                        else:
                            raise ValueError('Text does not conform to standards')
                    tagged.append((token.decode(PALAVRAS_ENCODING), syntactic_category))
            tagged_text = ' '.join([tuple2str(t) for t in tagged])
            msgout = {"database": msg['database'],
                      "collection": msg['collection'],
                      "spec": {"_id": msg['_id']},
                      "update": {"$set": {'tagged_text': tagged_text}},
                      "multi":False}
            self.sender.send_json(msgout)
        except ZMQError:
            self.sender.send_json({'fail': 1})