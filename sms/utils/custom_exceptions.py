from rest_framework import status
from rest_framework.exceptions import APIException

from sms.common import (
    messages as global_msg, constants as global_const
)

class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = global_msg.UNAUTHORIZED
    default_code = 'authentication_failed'

class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = global_msg.INTERNAL_SERVER_ERROR
    default_code = 'internal_server_error'


class VersionNotSupported(APIException):
    status_code = status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
    default_detail = global_msg.VERSION_NOT_SUPPORTED
    default_code = 'version_not_supported'


class ValidationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = global_msg.VALIDATION_FAILED
    default_code = 'validation_failed'


class ExpiredSignatureError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = global_msg.ACCESS_TOKEN_EXPIRED
    default_code = 'expired_signature_error'


class InvalidSignatureError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = global_msg.TOKEN_INVALID
    default_code = 'invalid_signature_error'


class DecodeError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = global_msg.DECODE_ERROR
    default_code = 'decode_error'


class InvalidTokenError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = global_msg.TOKEN_INVALID
    default_code = 'invalid_token_error'


class InvalidSlug(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = global_msg.INVALID_SLUG
    default_code = 'invalid_slug'

class RequestTimeout(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = global_msg.REQUEST_TIMEOUT
    default_code = 'request_timeout'