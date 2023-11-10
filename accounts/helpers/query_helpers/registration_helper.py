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
        user = User(
            email = data['email'],
            username = data['username'],
            password = hash_password(data['password']),
            first_name = data['first_name'],
            last_name = data['last_name'],
        )
        session.add(user)
        session.commit()

    except Exception as e:
        logger.error(f'registration_qh Query Function : {e}')
        session.rollback()

    return user