import bcrypt
import json
from redisary import Redisary


class AuthMiddleware:
    def __init__(self, get_response):
        self.tokens = Redisary(db=0)
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.json.get('password'):
            request.json['password'] = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())

        request.user = None
        if request.path not in ('/auth/login', '/auth/signup', '/'):
            token = request.COOKIES.get('token')
            if not token:
                raise Exception('Token dose not exist')
            if token not in self.tokens:
                raise Exception('Token dose not exist in the cache')

            request.user = json.loads(self.tokens[token])

        return self.get_response(request)
