import logging

from rest_framework.views import APIView
from rest_framework.versioning import NamespaceVersioning
from rest_framework.permissions import AllowAny

from sms.utils import custom_exceptions as ce
from sms.utils.custom_validators import CustomValidator
from sms.common import (messages as global_msg, constants as global_const)

from accounts.common import (constants as app_const)
from accounts.helpers.function_helpers.registration_helper import registration_fh

# Get an instance of logger
logger = logging.getLogger('accounts')

# Get an instance of Validator
c_validator = CustomValidator({}, allow_unknown = True)

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class RegistrationView(APIView):
    """
        User Registration
    """
    versioning_class = VersioningConfig
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
            [summary]
                Args:
                request (POST):
                email: Unique email address
                username: Unique username
                first_name
                last_name
                password: Min 8 characters
                confirm_password: Same as password
            Returns:
                json data: Serialize json data
        """

        try:
            if request.version == 'v1':
                schema = {
                    'email': {
                        'required': True,
                        'empty': False,
                        'type': 'string',
                        'isemail': True
                    },
                    'username': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'first_name': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'last_name': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'password': {
                        'required': True,
                        'empty': False,
                        'type': 'string',
                        'minlength': 8
                    },
                    'confirm_password': {
                        'required': True,
                        'empty': False,
                        'type': 'string',
                        'minlength': 8
                    },
                }

                is_valid = c_validator.validate(request.data, schema)
                if is_valid:
                    result = registration_fh(request)
                    return result
                
                else:
                    raise ce.ValidationFailed({
                        'message': global_msg.VALIDATION_FAILED,
                        'data': c_validator.errors
                    })
            
            else:
                raise ce.VersionNotSupported
        except ce.ValidationFailed as vf:
            logger.error(f'REGISTRATION API VIEW - POST : {vf}')
            raise

        except ce.VersionNotSupported as vns:
            logger.error(f'REGISTRATION API VIEW - POST : {vns}')
            raise

        except Exception as e:
            logger.error(f'REGISTRATION API VIEW - POST : {e}')
            raise ce.InternalServerError
