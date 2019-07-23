# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging, threading, uuid, requests, time

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from guacamole.client import GuacamoleClient

logger = logging.getLogger(__name__)
sockets = {}
sockets_lock = threading.RLock()
read_lock = threading.RLock()
write_lock = threading.RLock()
pending_read_request = threading.Event()
backendServer = "http://backend"

def index(request):
    if request.user.is_authenticated():
        command = requests.post(backendServer, json = str(request.user))
        print(command)
        return render(request, 'core/index.html', {})
    else:
        return HttpResponse("Something went wrong")


@csrf_exempt
def tunnel(request):
    qs = request.META['QUERY_STRING']
    logger.info('tunnel %s', qs)
    if qs == 'connect':
        return _do_connect(request)
    else:
        tokens = qs.split(':')
        if len(tokens) >= 2:
            if tokens[0] == 'read':
                return _do_read(request, tokens[1])
            elif tokens[0] == 'write':
                return _do_write(request, tokens[1])

    return HttpResponse(status=400)

def _do_connect(request):
    # Connect to guacd daemon
    vcdUser = str(request.user)
    client = GuacamoleClient('guacd', 4822)
    #command = requests.get(backendServer)
    #logging.warning(str(command.content))
    #if not vcdUser in command.content:
    #    logging.warning("sleeping 2 seconds")
    time.sleep(2)
    #logging.warning("continueeeee")
    client.handshake(protocol='rdp',
            hostname='vcd-' + vcdUser,
            port=3389,
            username= vcdUser,
            password= vcdUser,
            width=request.POST.get("width"),
            height=request.POST.get("height"))
    cache_key = str(uuid.uuid4())
    with sockets_lock:
        logger.info('Saving socket with key %s', cache_key)
        sockets[cache_key] = client

    response = HttpResponse(content=cache_key)
    response['Cache-Control'] = 'no-cache'
    return response


def _do_read(request, cache_key):
    pending_read_request.set()

    def content():
        with sockets_lock:
            client = sockets[cache_key]

        with read_lock:
            pending_read_request.clear()

            while True:
                # instruction = '5.mouse,3.400,3.500;'
                instruction = client.receive()
                if instruction:
                    yield instruction
                else:
                    break

                if pending_read_request.is_set():
                    logger.info('Letting another request take over.')
                    break

            # End-of-instruction marker
            yield '0.;'

    response = StreamingHttpResponse(content(),
                                     content_type='application/octet-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def _do_write(request, cache_key):
    with sockets_lock:
        client = sockets[cache_key]

    with write_lock:
        while True:
            chunk = request.read(8192)
            if chunk:
                client.send(chunk)
            else:
                break

    response = HttpResponse(content_type='application/octet-stream')
    response['Cache-Control'] = 'no-cache'
    return response
