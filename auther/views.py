import json
from base64 import b85encode
from os import urandom

import bcrypt
from django.http import HttpResponseBadRequest, JsonResponse
from redisary import Redisary

from auther.models import User

tokens = Redisary(db=0)


def login(request):
    if not request.json:
        return HttpResponseBadRequest()

    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return HttpResponseBadRequest()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Exception(f'Username not found')
    roles = user.roles.all()

    if bcrypt.checkpw(password.encode('utf-8'), bytes(user.password)):
        token = b85encode(urandom(26))
        token = str(token, encoding='utf-8')
        payload = {
            'id': user.id,
            'name': user.name,
            'pic_id': user.pic_id,
            'perms': [role.name for role in roles]
        }
        tokens[token] = json.dumps(payload)

        response = JsonResponse(payload)
        response.set_cookie('token', token, max_age=7 * 60 * 60 * 24)
        return response

    raise Exception(f'Wrong password')
