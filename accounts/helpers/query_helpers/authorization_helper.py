import logging
from sms.database import session
from accounts.models import User

from sms.utils.data_formatter import (
    result_list_to_dict, result_row_to_dict
)

from accounts.utils.passwords import verify_password

# Get an instance of logger
logger = logging.getLogger('accounts')

def get_user_qh(user_id: int):
    """
        Get user from user_id
    """
    try:
        user = session.query(
            User.id,
            User.email,
            User.username,
            User.first_name,
            User.last_name,
            User.profile_picture,
            User.is_active,
            User.gender,
            User.role,
            User.dob,
            User.address,
            User.created_at,
            User.updated_at,
        ).filter(
            User.id == user_id,
            User.is_active == 1
        ).one_or_none()
        session.commit()

        if user:
            user = result_row_to_dict(user)
            user = User(**user)

    except Exception as e:
        logger.error(f'get_user_qh Query Function : {e}')
        session.rollback()
        user = None

    return user

def get_user_with_email_password_qh(email: str, password: str):
    """
        Get user from email and password
    """
    try:
        user = session.query(
            User.id,
            User.password,
            User.role
        ).filter(
            User.email == email,
            User.is_active == 1
        ).one_or_none()
        session.commit()

        if user and verify_password(password, user.password):
            user = result_row_to_dict(user)

    except Exception as e:
        logger.error(f'get_user_with_email_password_qh Query Function : {e}')
        session.rollback()
        user = None

    return user
