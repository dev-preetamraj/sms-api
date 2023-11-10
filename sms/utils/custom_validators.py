import re
import datetime
from cerberus import Validator
import json

from sms.common import (
    messages as global_msg, constants as global_const
)

class CustomValidator(Validator):
    # Validate Numeric
    def _validate_isnumeric(self, isnumeric, field, value):
        """
        {'type':'boolean'}
        """
        if isnumeric:
            try:
                number = int(value)
            except Exception:
                self._error(field, global_msg.INTEGER_ONLY)


    # Validate starting ending spaces in string
    def _validate_emptystring(self, emptystring, field, value):
        """
        {'type':'boolean'}
        """
        if emptystring:
            characters_count = sum(not chr.isspace() for chr in value)

            if characters_count == 0:
                self._error(field, global_msg.EMPTY_STRING_VALIDATION)

    # Validate aadhaar card
    def _validate_isaadhaar(self, isaadhaar, field, value):
        """
        {'type':'boolean'}
        """
        if isaadhaar:
            isaadhaar_reg = re.match('^[0-9]{12}$', value)

            if not isaadhaar_reg:
                self._error(field, global_msg.INVALID_AADHAAR_NUMBER)

    # Validate Alpha Numeric
    def _validate_isalphanumeric(self, isalphanumeric, field, value):
        """
        {'type':'boolean'}
        """
        if isalphanumeric:
            zeroes = re.match('^0+$', value)
            if zeroes:
                self._error(
                    field, global_msg.INVALID_ALPHANUMERIC)

            alphanumeric_id = re.match('^(?![0-9_ -]*$)[a-zA-Z0-9_ -]+$', value)

            if not alphanumeric_id:
                self._error(
                    field, global_msg.INVALID_ALPHANUMERIC)

    # Validate Empty string in List
    def _validate_islistempty(self, islistempty, field, value):
        """
        {'type':'boolean'}
        """
        if islistempty and '' in value:
            self._error(
                field, global_msg.EMPTY_STRING_IN_LIST_NOT_ALLOWED
            )

    # Validate If a string is boolean
    def _validate_isboolean(self, isboolean, field, value):
        """
        {'type':'boolean'}
        """
        if isboolean:
            try:
                value = json.loads(value.lower())
            except Exception:
                self._error(field, global_msg.INVALID_BOOLEAN)


    # Validate Date Format - DD-MM-YYYY
    def _check_with_disbursaldateformat(self, field, value):
        """
        {'check_with': 'disbursaldateformat'}
        """
        format_string = '%d-%m-%Y'

        try:
            datetime.datetime.strptime(value, format_string)
        except Exception:
            self._error(field, global_msg.DISBURSAL_DATE_FORMAT_INVALID)


    # Validate Email
    def _validate_isemail(self, isemail, field, value):
        """
        {'type': 'boolean'}
        """
        if isemail:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            match_status = re.match(regex, value)

            if not match_status:
                self._error(field, global_msg.INVALID_EMAIL_ADDRESS)


    # Validate First and Last Character of String is Space
    def _validate_isflspace(self, isflspace, field, value):
        """
        {'type': 'boolean'}
        """
        if isflspace:
            first_char = value[0]
            last_char = value[-1]

            if first_char.isspace() or last_char.isspace():
                self._error(field, global_msg.FL_SPACE_VALIDATION)