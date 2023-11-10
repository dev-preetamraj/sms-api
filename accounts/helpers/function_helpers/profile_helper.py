import logging
from rest_framework.response import Response
from rest_framework import status
from sms.utils import custom_exceptions as ce
from sms.common import (messages as global_msg, constants as global_const)

from accounts.common import (messages as app_msg, constants as app_const)
from accounts.models import User

# Get an instance of logger
logger = logging.getLogger('accounts')

def fetch_user_profile_fh(request):
    """
        Fetch user profile
    """
    try:
        user = request.user.as_dict()
        user.pop('password')
        
        return Response({
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': app_msg.USER_FETCHED_SUCCESS,
            'data': user},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f'fetch_user_profile_fh Helper Function : {e}')
        raise ce.InternalServerError
