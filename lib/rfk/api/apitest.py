import rfk
from rfk.site import db
from rfk.api import api, check_auth, wrapper
from flask import jsonify, request, g


# DEBUG
@api.route('/web/gen_testdata')
def gen_testdata():
    user = rfk.User('MrLoom', rfk.User.make_password('keks'), rfk.User.make_password('keks'))
    db.session.add(user)
    
    key = rfk.ApiKey(1, 'Test')
    key.gen_key(db.session)
    db.session.add(key)
    
    db.session.commit()
    return key.key
# DEBUG

@api.route('/web/dj')
@check_auth()
def dj():
    id = request.args.get('id', None)
    name = request.args.get('name', None)
    
    if id:
        result = db.session.query(rfk.User).get(id)
    elif name:
        result = db.session.query(rfk.User).filter(rfk.User.name == name).first()
    else:
        return jsonify(wrapper(None, 400, 'missing required query parameter'))
    
    if result:
        data = {'dj': {'id': result.user, 'name': result.name, 'status': result.status}}
    else:
        data = {'dj': None}
    return jsonify(wrapper(data))

@api.route('/web/current_dj')
@check_auth()
def current_dj():
    result = db.session.query(rfk.User).filter(rfk.User.status == rfk.User.STATUS_STREAMING).first()
    if result:
        data = {'current_dj': {'id': result.user, 'name': result.name, 'status': result.status}} 
    else:
        data = {'current_dj': None}
    return jsonify(wrapper(data))

@api.route('/web/kick_dj')
@check_auth(required_permissions=[rfk.ApiKey.FLAGS.KICK])
def kick_dj():
    return "TODO"

