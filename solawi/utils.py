import datetime

def date_from_week(week=None, year=None):
    if year is None:
        year = datetime.date.today().year
    if week is None:
        week = datetime.date.today().strftime('%W')
    dstr = '{}-{}-1'.format(year, week)
    return datetime.datetime.strptime(dstr, '%Y-%W-%w')
