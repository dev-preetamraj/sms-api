import logging

from rest_framework.views import APIView
from rest_framework.versioning import NamespaceVersioning
from rest_framework.permissions import AllowAny

from sms.utils import custom_exceptions as ce
from sms.utils.custom_validators import CustomValidator
from sms.common import (messages as global_msg, constants as global_const)

from accounts.common import (constants as app_const)
from accounts.helpers.function_helpers.profile_helper import fetch_user_profile_fh

# Get an instance of logger
logger = logging.getLogger('accounts')

# Get an instance of Validator
c_validator = CustomValidator({}, allow_unknown = True)

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class ProfileView(APIView):
    """
        Profile of an user
    """
    versioning_class = VersioningConfig
    
    def get(self, request):
        """
            [summary]
                Args:
                request (GET):
            Returns:
                json data: Serialize json data
        """
        try:
            if request.version == 'v1':
                schema = {}
                is_valid = c_validator.validate(request.data, schema)
                if is_valid:
                    result = fetch_user_profile_fh(request)
                    return result
                    
                else:
                    raise ce.ValidationFailed({
                        'message': global_msg.VALIDATION_FAILED,
                        'data': c_validator.errors
                    })

            else:
                raise ce.VersionNotSupported
        except ce.ValidationFailed as vf:
            logger.error(f'Profile API VIEW - GET : {vf}')
            raise

        except ce.VersionNotSupported as vns:
            logger.error(f'Profile API VIEW - GET : {vns}')
            raise

        except Exception as e:
            logger.error(f'Profile API VIEW - GET : {e}')
            raise ce.InternalServerError
