import logging
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from sms.utils import custom_exceptions as ce
from sms.common import (messages as global_msg, constants as global_const)

from accounts.common import (messages as app_msg, constants as app_const)
from accounts.helpers.query_helpers.authorization_helper import get_user_with_email_password_qh, get_user_qh

# Get an instance of logger
logger = logging.getLogger('accounts')

def authorize_fh(request, slug):
    """
        Authorization
    """
    try:
        if slug == "authorize":
            email = request.data.get('email')
            password = request.data.get('password')
            user = get_user_with_email_password_qh(email, password)

            if user['role'].value != request.data.get('role'):
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': global_msg.INVALID_ROLE_REQUEST,
                    'data': None
                }, status = status.HTTP_400_BAD_REQUEST)

            if user:
                access_token = generate_access_token(user['id'], user['role'].value)
                refresh_token = generate_refresh_token(user['id'], user['role'].value)

                return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': global_msg.ACCESS_GRANTED,
                    'data': {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    },
                }, status = status.HTTP_200_OK)

            return Response({
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': app_msg.USER_NOT_FOUND,
                'data': None,
            }, status = status.HTTP_401_UNAUTHORIZED)

        elif slug == "refresh-token":
            return regenerate_token(request.data.get('refresh_token'))
        elif slug == 'verify-token':
            return verify_token(request.data.get('access_token'))
        
    except Exception as e:
        logger.error(f'authorize_fh Helper Function : {e}')
        raise ce.InternalServerError

def generate_access_token(user_id, role):
    access_token_payload = {
        'user_id': user_id,
        'role': role,
        'exp': (
            datetime.utcnow() +
            timedelta(
                days=0, minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES
            )
        ),
        'iat': datetime.utcnow(),
    }

    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    )

    return access_token


def generate_refresh_token(user_id, role):
    refresh_token_payload = {
        'user_id': user_id,
        'role': role,
        'exp': (
            datetime.utcnow() +
            timedelta(
                days=settings.REFRESH_TOKEN_EXPIRY_DAYS
            )
        ),
        'iat': datetime.utcnow()
    }

    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_SECRET_KEY, algorithm='HS256'
    )

    return refresh_token


def regenerate_token(refresh_token):
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_SECRET_KEY, algorithms=['HS256']
        )

        user = get_user_qh(payload.get('user_id'))

        if user:
            return Response({
                "success" : True,
                "status_code" :status.HTTP_201_CREATED,
                "message" : global_msg.ACCESS_TOKEN_REGENERATED,
                'data': {
                    'access_token': generate_access_token(
                        user.id,
                        user.role.value
                    )
                },
            }, status = status.HTTP_201_CREATED)

        return Response({
                "success" : False,
                "status_code" :status.HTTP_404_NOT_FOUND,
                "message" : app_msg.USER_NOT_FOUND,
                "data" : None
            }, status = status.HTTP_404_NOT_FOUND)


    except jwt.ExpiredSignatureError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.REFRESH_TOKEN_EXPIRED,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)

    except jwt.InvalidSignatureError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.TOKEN_INVALID,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)

    except jwt.DecodeError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.DECODE_ERROR,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)

    except jwt.InvalidTokenError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.TOKEN_INVALID,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)
    
def verify_token(access_token):
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256']
        )

        user = get_user_qh(payload.get('user_id'))

        if user.role.value != payload.get('role'):
            return Response({
                "success" : False,
                "status_code" :status.HTTP_400_BAD_REQUEST,
                "message" : global_msg.INVALID_ROLE_REQUEST,
                'data': None
            }, status = status.HTTP_400_BAD_REQUEST)
        
        if user:
            return Response({
                "success" : True,
                "status_code" :status.HTTP_200_OK,
                "message" : global_msg.ACCESS_TOKEN_VERIFIED,
                'data': None
            }, status = status.HTTP_200_OK)

        return Response({
                "success" : False,
                "status_code" :status.HTTP_404_NOT_FOUND,
                "message" : app_msg.USER_NOT_FOUND,
                "data" : None
            }, status = status.HTTP_404_NOT_FOUND)


    except jwt.ExpiredSignatureError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.REFRESH_TOKEN_EXPIRED,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)

    except jwt.InvalidSignatureError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.TOKEN_INVALID,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)

    except jwt.DecodeError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.DECODE_ERROR,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)

    except jwt.InvalidTokenError:
        return Response({
            "success" : False,
            "status_code" :status.HTTP_401_UNAUTHORIZED,
            "message" : global_msg.TOKEN_INVALID,
            "data" : None
        }, status = status.HTTP_401_UNAUTHORIZED)