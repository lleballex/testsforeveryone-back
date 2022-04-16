from django.conf import settings

import jwt


def encode_auth_token(user_id):
    return jwt.encode({
        'user_id': user_id,
    }, settings.SECRET_KEY)


def decode_auth_token(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['user_id']
    except jwt.exceptions.DecodeError as e:
        return None