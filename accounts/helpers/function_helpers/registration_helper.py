import logging
from rest_framework.response import Response
from rest_framework import status
from sms.utils import custom_exceptions as ce
from sms.common import (messages as global_msg, constants as global_const)

from accounts.common import (messages as app_msg, constants as app_const)
from accounts.helpers.query_helpers.registration_helper import registration_qh
from accounts.helpers.query_helpers.user_helper import get_user_by_email_qh, get_user_by_username_qh

# Get an instance of logger
logger = logging.getLogger('accounts')

def registration_fh(request):
    """
        User Registration
    """
    try:
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if get_user_by_email_qh(request.data.get('email')):
            return Response({
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': app_msg.EMAIL_NOT_UNIQUE,
                'data': None
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if get_user_by_username_qh(request.data.get('username')):
            return Response({
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': app_msg.USERNAME_NOT_UNIQUE,
                'data': None
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            return Response({
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': app_msg.PASSWORD_NOT_MATCHED,
                'data': None
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        user = registration_qh(request.data)
        user = user.as_dict()
        user.pop('password')
        return Response({
            'success': True,
            'status_code': status.HTTP_201_CREATED,
            'message': app_msg.REGISTRATION_SUCCESS,
            'data': user
            }, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        logger.error(f'registration_fh Helper Function : {e}')
        raise ce.InternalServerError
