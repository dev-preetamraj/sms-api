import logging
from sms.database import session

from accounts.models import User
from accounts.utils.passwords import hash_password
from sms.utils.data_formatter import result_row_to_dict

# Get an instance of logger
logger = logging.getLogger('accounts')

def registration_qh(data):
    """
        User Registration
    """
    try:
        data.pop('confirm_password')
        data['password'] = hash_password(data['password'])
        user = User(**data)
        session.add(user)
        session.commit()

    except Exception as e:
        logger.error(f'registration_qh Query Function : {e}')
        session.rollback()

    return user