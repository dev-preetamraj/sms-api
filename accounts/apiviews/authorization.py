import logging

from rest_framework.views import APIView
from rest_framework.versioning import NamespaceVersioning
from rest_framework.permissions import AllowAny

from sms.utils import custom_exceptions as ce
from sms.utils.custom_validators import CustomValidator
from sms.common import (messages as global_msg, constants as global_const)

from accounts.common import (constants as app_const)
from accounts.helpers.function_helpers.authorization_helper import authorize_fh

# Get an instance of logger
logger = logging.getLogger('accounts')

# Get an instance of Validator
c_validator = CustomValidator({}, allow_unknown = True)

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class AuthorizationView(APIView):
    """
        Authorization of user
    """
    versioning_class = VersioningConfig
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, slug):
        """
            [summary]
                Args:
                request (POST):
                email: Email address
                password: Password of user
            Returns:
                json data: Serialize json data
        """
        try:
            if request.version == 'v1':
                if slug == 'authorize':
                    schema = {
                        'email': {
                            'required': True,
                            'empty': False,
                            'type': 'string',
                            'isemail': True
                        },
                        'password': {
                            'required': True,
                            'empty': False,
                            'type': 'string',
                            'minlength': 8
                        },
                        'role': {
                            'required': True,
                            'empty': False,
                            'type': 'string',
                            'isrole': True
                        }
                    }
                
                elif slug == "refresh-token":
                    schema = {
                        'refresh_token': {
                            'required': True,
                            'empty': False,
                            'type': 'string',
                            'isflspace': True
                        }
                    }
                
                elif slug == "verify-token":
                    schema = {
                        'access_token': {
                            'required': True,
                            'empty': False,
                            'type': 'string',
                            'isflspace': True
                        }
                    }

                else:
                    raise ce.InvalidSlug

                is_valid = c_validator.validate(request.data, schema)
                if is_valid:
                    result = authorize_fh(request, slug)
                    return result
                else:
                    raise ce.ValidationFailed({
                        'message': global_msg.VALIDATION_FAILED,
                        'data': c_validator.errors
                    })

            else:
                raise ce.VersionNotSupported
        except ce.ValidationFailed as vf:
            logger.error(f'Authorization API VIEW - POST : {vf}')
            raise

        except ce.VersionNotSupported as vns:
            logger.error(f'Authorization API VIEW - POST : {vns}')
            raise

        except Exception as e:
            logger.error(f'Authorization API VIEW - POST : {e}')
            raise ce.InternalServerError
