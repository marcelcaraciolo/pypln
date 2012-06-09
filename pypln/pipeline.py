#!/usr/bin/env python
# coding: utf-8

from logging import Logger, NullHandler
from copy import deepcopy
from pypln.client import ManagerClient


class Worker(object):
    def __init__(self, worker_name):
        self.name = worker_name
        self.after = []

    def then(self, *after):
        self.after = after
        return self

class Pipeline(object):
    def __init__(self, pipeline, api_host_port, broadcast_host_port,
                 logger=None, logger_name='Pipeline', time_to_wait=0.1):
        self.client = ManagerClient(logger, logger_name)
        self.client.connect(api_host_port, broadcast_host_port)
        self.pipeline = pipeline
        self.time_to_wait = time_to_wait
        self.logger = self.client.logger

    def send_job(self, worker):
        job = {'command': 'add job', 'worker': worker.name,
               'document': worker.document}
        self.client.send_api_request(job)
        self.logger.info('Sent job: {}'.format(job))
        message = self.client.get_api_reply()
        subscribe_message = 'job finished: {}'.format(message['job id'])
        self.client.broadcast_subscribe(subscribe_message)
        self.logger.info('Received from Manager API: {}'.format(message))
        self.waiting[message['job id']] = worker

    def distribute(self):
        self.waiting = {}
        for document in self.documents:
            worker = deepcopy(self.pipeline)
            worker.document = document
            self.send_job(worker)

    def run(self, documents):
        self.documents = documents
        self.distribute()
        try:
            while True:
                if self.client.broadcast_poll(self.time_to_wait):
                    message = self.client.broadcast_receive()
                    self.logger.info('[Client] Received from broadcast: {}'\
                                     .format(message))
                    if message.startswith('job finished: '):
                        job_id = message.split(': ')[1].split(' ')[0]
                        if job_id in self.waiting:
                            message = 'job finished: {}'.format(job_id)
                            self.client.broadcast_unsubscribe(message)
                            worker = self.waiting[job_id]
                            for next_worker in worker.after:
                                next_worker.document = worker.document
                                self.send_job(next_worker)
                            del self.waiting[job_id]
                if not self.waiting.keys():
                    break
        except KeyboardInterrupt:
            self.client.close_sockets()

def main():
    import os
    import shlex
    from logging import Logger, StreamHandler, Formatter
    from sys import stdout, argv
    from pymongo import Connection
    from gridfs import GridFS


    if len(argv) == 1:
        print 'ERROR: you need to pass files to import'
        exit(1)

    api_host_port = ('localhost', 5555)
    broadcast_host_port = ('localhost', 5556)
    #TODO: should get config from manager
    config = {'db': {'host': 'localhost', 'port': 27017,
                     'database': 'pypln',
                     'collection': 'documents',
                     'gridfs collection': 'files',
                     'monitoring collection': 'monitoring'},
              'monitoring interval': 60,}
    db_config = config['db']
    mongo_connection = Connection(db_config['host'], db_config['port'])
    db = mongo_connection[db_config['database']]
    if 'username' in db_config and 'password' in db_config and \
            db_config['username'] and db_config['password']:
           db.authenticate(db_config['username'], db_config['password'])
    gridfs = GridFS(db, db_config['gridfs collection'])
    #TODO: connection/collection lines should be in pypln.stores.mongodb

    logger = Logger('Pipeline')
    handler = StreamHandler(stdout)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                          '%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    my_docs = []
    filenames = shlex.split(' '.join(argv[1:]))
    logger.info('Inserting files...')
    for filename in filenames:
        if os.path.exists(filename):
            logger.info('  {}'.format(filename))
            file_object = open(filename)
            doc_id = gridfs.put(file_object.read(), filename=filename)
            my_docs.append(str(doc_id))
            file_object.close()
        else:
            logger.info('  Ignoring {} (file not found)'.format(filename))

    #TODO: use et2 to create the tree/pipeline image
    W, W.__call__ = Worker, Worker.then
    workers = W('extractor')(W('tokenizer')(W('pos'),
                                            W('freqdist')))
    pipeline = Pipeline(workers, api_host_port, broadcast_host_port, logger)
    pipeline.run(my_docs)
    #TODO: should receive a 'job error' from manager when some job could not be
    #      processed (timeout, worker not found etc.)


if __name__ == '__main__':
    main()
