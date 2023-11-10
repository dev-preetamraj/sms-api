import logging
from sms.database import session

from accounts.models import User

# Get an instance of logger
logger = logging.getLogger('accounts')

def get_user_by_username_qh(username):
    """
        Get user by username
    """
    try:
        user = session.query(
            User.id
        ).filter(
            User.username == username
        ).one_or_none()
        session.commit()

    except Exception as e:
        logger.error(f'get_user_by_username_qh Query Function : {e}')
        session.rollback()
        user = None

    return user

def get_user_by_email_qh(email):
    """
        Get user by email
    """
    try:
        user = session.query(
            User.id
        ).filter(
            User.email == email
        ).one_or_none()
        session.commit()

    except Exception as e:
        logger.error(f'get_user_by_email_qh Query Function : {e}')
        session.rollback()
        user = None

    return user