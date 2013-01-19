'''
Created on Aug 11, 2012

@author: teddydestodes
'''

from flask import Blueprint, request, make_response
import logging
from rfk.database.streaming import Relay, Stream, StreamRelay, Listener
from rfk.database import session


log = logging.getLogger('werkzeug')

backend = Blueprint('icecast',__name__)

@backend.route('/icecast/auth', methods=['POST'])
def icecast_auth():
    if request.form['action'] != 'stream_auth':
        return make_response('you just went full retard', 405)
    relay = Relay.get_relay(address=request.form['server'],
                            port=request.form['port'])
    if relay.auth_password == request.form['pass'] and\
       relay.auth_username == request.form['user']:
        return make_response('ok', 200, {'icecast-auth-user': '1'})
    else:
        return make_response('authentication failed', 401)
    
@backend.route('/icecast/add', methods=['POST'])
def icecast_add_mount():
    if request.form['action'] != 'mount_add':
        return make_response('you just went full retard', 405)
    relay = Relay.get_relay(address=request.form['server'],
                            port=request.form['port'])
    stream = Stream.get_stream(mount=request.form['mount'])
    if relay and stream:
        stream.add_relay(relay)
        relay.get_stream_relay(stream).status = StreamRelay.STATUS.ONLINE
        session.commit()
        return make_response('ok', 200, {'icecast-auth-user': '1'})
    else:
        return make_response('something strange happened', 500)
    
@backend.route('/icecast/remove', methods=['POST'])
def icecast_remove_mount():
    if request.form['action'] != 'mount_remove':
        return make_response('you just went full retard', 405)
    relay = Relay.get_relay(address=request.form['server'],
                            port=request.form['port'])
    stream = Stream.get_stream(mount=request.form['mount'])
    if relay and stream:
        stream.add_relay(relay)
        stream_relay = relay.get_stream_relay(stream)
        stream_relay.set_offline()
        session.commit()
        return make_response('ok', 200, {'icecast-auth-user': '1'})
    else:
        return make_response('something strange happened', 500)

@backend.route('/icecast/listenerremove', methods=['POST'])
def icecast_remove_listener():
    log.warning(request.form)
    if request.form['action'] != 'listener_remove':
        return make_response('you just went full retard', 405)
    relay = Relay.get_relay(address=request.form['server'],
                            port=request.form['port'])
    stream = Stream.get_stream(mount=request.form['mount'])
    listener = Listener.get_listener(relay.get_stream_relay(stream), int(request.form['client']))
    listener.set_disconnected()
    session.commit()
    return make_response('ok', 200, {'icecast-auth-user': '1'})

@backend.route('/icecast/listeneradd', methods=['POST'])
def icecast_add_listener():
    
    if request.form['action'] != 'listener_add':
        return make_response('you just went full retard', 405)
    relay = Relay.get_relay(address=request.form['server'],
                            port=request.form['port'])
    stream = Stream.get_stream(mount=request.form['mount'])
    listener = Listener.create(request.form['ip'], request.form['client'], request.form['agent'], relay.get_stream_relay(stream))
    session.add(listener)
    session.commit()
    return make_response('ok', 200, {'icecast-auth-user': '1'})