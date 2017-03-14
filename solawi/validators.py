from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import json


def portion_account_validate(value):
    try:
        j = json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError(
            _('%(value)s is not a valid json.'),
            params={'value': value},)
    else:
        for week, portion in j.items():
            week = int(week)
            if not isinstance(portion, int) or portion < 0:
                raise ValidationError(
                    _('%(value)s contains a wrong portion'),
                    params={'value': value,})
