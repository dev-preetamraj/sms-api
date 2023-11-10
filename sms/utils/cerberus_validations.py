import re

from sms.common import messages as global_msg


def validate_pincode(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    """
    if not re.match("^[1-9]{1}[0-9]{2}[0-9]{3}$", value):
        error(field, global_msg.INVALID_PINCODE)


def validate_pancard(field, value, error):
    """ validate of pan card number

    The rule's arguments are validated against this schema:
    """

    if not re.match(r'[A-Z]{5}[0-9]{4}[A-Z]{1}$', value):
        error(field, global_msg.INVALID_PAN_CARD_NUMBER)


def validate_bank_account_number(field, value, error):
    """ Test the oddity of a value.

    The rule's arguments are validated against this schema:
    """
    # '^[0-9]{9,18}$'
    if not re.match(r'^\d{9,18}$', value):
        error(field, global_msg.INVALID_BANK_ACCOUNT_NUMBER)


def validate_ifsc(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    """
    if not re.match('^[A-Z]{4}0[A-Z0-9]{6}$', value):
        error(field, global_msg.INVALID_IFSC)


def validate_voter_id(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    """
    if not re.match('^([a-zA-Z]){3}([0-9]){7}?$', value):
        error(field, global_msg.INVALID_VOTER_ID)


def validate_passport_number(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    """
    if not re.match('^(?!^0+$)[a-zA-Z0-9]{3,20}$', value):
        error(field, global_msg.INVALID_PASSPORT_NUMBER)


def validate_date_format(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    Validating date format to DD/MM/YYYY
    """
    if not re.match(
            '^(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/[0-9]{4}$', value):
        error(field, global_msg.INVALID_DATE_FORMAT)


def validate_aadhaar(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    Validating date format to DD/MM/YYYY
    """
    if not re.match(
            '^[0-9]{12}$', value):
        error(field, global_msg.INVALID_AADHAAR_NUMBER)

def validate_payment_type(field,value,error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    validating payment type upfront or emi 
    """
    payment_type_list = ['UPFRONT','EMI']
    if value not in payment_type_list:
        error(field,global_msg.INVALID_PAYMENT_TYPE)

def validate_captcha(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    validating payment type upfront or emi
    """
    if not re.match(
            '^[a-zA-Z0-9]{6,}$', value):
        error(field, global_msg.INVALID_CAPTCHA_CODE)

def validate_empty_string(field, value, error):
    """ Test the oddity of a value.
    - , _, @, ., /, #, &, +
    The rule's arguments are validated against this schema:
    validating payment type upfront or emi
    """
    if not re.match(
            '^[^\s]+(\s.*)?$', value):
        error(field, global_msg.EMPTY_STRING_VALIDATION)