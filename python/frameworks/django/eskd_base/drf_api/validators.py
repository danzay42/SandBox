from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_decimal_number(value):
    dn_pattern_main = r'[A-ZА-Я]{4}\.\d{6}\.\d{3}'
    dn_pattern_tail = r'(-\d{,3})?'

    match = re.fullmatch(dn_pattern_main+dn_pattern_tail, value)

    if not match:
        raise ValidationError(
            _('%(value)s bad decimal number'),
            params={'decimal number': value},
        )
    return value