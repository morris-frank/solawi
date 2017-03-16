import datetime


def this_year():
    return datetime.date.today().year


def this_week():
    return int(datetime.date.today().strftime('%W'))


def date_from_week(week=None, year=None):
    if year is None:
        year = this_year()
    if week is None:
        week = this_week()
    dstr = '{}-{}-1'.format(year, week)
    return datetime.datetime.strptime(dstr, '%Y-%W-%w')
