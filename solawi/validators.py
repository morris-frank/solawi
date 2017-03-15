import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import json


def portion_account_validate(value):
    try:
        j = json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError(
            _('{v} is not a valid JSON.').format(v=value),
            params={'value': value},)
    else:
        if not isinstance(j, list):
            raise ValidationError(
                _('The Account is just a list of tuples'
                  ' [year, week, assets].'),
                params={'value': value},)
        for i in j:
            if not isinstance(i, list) or len(i) < 3:
                raise ValidationError(
                    _('{i} is not a list in the form of'
                      ' [year, week, assets].').format(i=i),
                    params={'value': value},)
            (year, week, asset) = i
            if not isinstance(year, int) or year < datetime.MINYEAR or year > datetime.MAXYEAR:
                raise ValidationError(
                    _('{y} is not a year number.').format(y=year),
                    params={'value': value},)
            if not isinstance(week, int) or week > 53 or week < 0:
                raise ValidationError(
                    _('{w} is not a week number.').format(w=week),
                    params={'value': value},)
            if not isinstance(asset, int) or asset < 0:
                raise ValidationError(
                    _('{v} is not a valid asset').format(v=asset),
                    params={'value': value},)
