import datetime


def view_property(method):
    @property
    def method_wrapper(self, *args, **kwargs):
        prop_name = '_' + method.__name__
        if prop_name not in self.__dict__:
            self.__dict__[prop_name] = method(self, *args, **kwargs)
        return self.__dict__[prop_name]
    return method_wrapper


def get_moday(date):
    return date - datetime.timedelta(date.weekday())


def this_year():
    return datetime.date.today().year


def this_week():
    return int(datetime.date.today().strftime('%W'))


def date_from_week(year=None, week=None):
    if year is None:
        year = this_year()
    if week is None:
        week = this_week()
    dstr = '{year}-{week}-1'.format(year=year, week=week)
    return datetime.datetime.strptime(dstr, '%Y-%W-%w')
