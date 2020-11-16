import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


class UsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9._-]+\Z'
    message = 'Only a-z, A-Z, 0-9 and (.), (_), (-) are allowed.'
    code = 'INVALID_USERNAME'
    flags = 0


@deconstructible
class EmailValidator:
    __message = 'Allowed email address domains [ gmail.com, icloud.com, outlook.com, protonmail.com, yahoo.com ].'
    __code = 'INVALID_EMAIL_ADDRESS'
    __whitelist = ['gmail.com', 'icloud.com', 'outlook.com', 'protonmail.com', 'yahoo.com']
    __email_username_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',
        flags=re.IGNORECASE
    )

    def __init__(self):
        if settings.DEBUG:
            self.__whitelist.append('localhost')

    def __call__(self, value):
        if '@' not in value:
            raise ValidationError(message=self.__message, code=self.__code)

        email_username_part, email_domain_part = value.rsplit('@', 1)
        if self.__email_username_regex.match(email_username_part) and email_domain_part in self.__whitelist:
            return
        raise ValidationError(message=self.__message, code=self.__code)

    def __eq__(self, other):
        return isinstance(other, EmailValidator)
