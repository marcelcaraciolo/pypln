#!/usr/bin/env python
# coding: utf-8

from logging import Logger, NullHandler
import zmq


class ManagerClient(object):
    def __init__(self, logger=None, logger_name='ManagerClient'):
        self.context = zmq.Context()
        if logger is None:
            self.logger = Logger(logger_name)
            self.logger.addHandler(NullHandler())
        else:
            self.logger = logger

    def connect(self, api_host_port, broadcast_host_port):
        self.api_host_port = api_host_port
        self.broadcast_host_port = broadcast_host_port
        self.api_connection_string = 'tcp://{}:{}'.format(*api_host_port)
        self.broadcast_connection_string = \
                'tcp://{}:{}'.format(*broadcast_host_port)

        self.manager_api = self.context.socket(zmq.REQ)
        self.manager_broadcast = self.context.socket(zmq.SUB)

        self.manager_api.connect(self.api_connection_string)
        self.manager_broadcast.connect(self.broadcast_connection_string)

    def send_api_request(self, json):
        self.manager_api.send_json(json)

    def get_api_reply(self):
        return self.manager_api.recv_json()

    def broadcast_subscribe(self, subscribe_to):
        return self.manager_broadcast.setsockopt(zmq.SUBSCRIBE, subscribe_to)

    def broadcast_unsubscribe(self, unsubscribe_to):
        return self.manager_broadcast.setsockopt(zmq.UNSUBSCRIBE,
                                                 unsubscribe_to)

    def broadcast_poll(self, timeout=0):
        return self.manager_broadcast.poll(timeout)

    def broadcast_receive(self):
        return self.manager_broadcast.recv()

    def __del__(self):
        self.close_sockets()

    def close_sockets(self):
        sockets = ['manager_api', 'manager_broadcast']
        for socket in sockets:
            if hasattr(self, socket):
                getattr(self, socket).close()
