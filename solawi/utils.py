import copy
import datetime

def view_property(method):
    '''

    Args:
      method:

    Returns:

    '''
    @property
    def method_wrapper(self, *args, **kwargs):
        '''

        Args:
          *args:
          **kwargs:

        Returns:

        '''
        prop_name = '_' + method.__name__
        if prop_name not in self.__dict__:
            self.__dict__[prop_name] = method(self, *args, **kwargs)
        return self.__dict__[prop_name]
    return method_wrapper


def get_moday(date=None):
    '''

    Args:
      date:

    Returns:

    '''
    if date is None:
        date = datetime.date.today()
    return date - datetime.timedelta(date.weekday())


def this_year():
    ''' '''
    return datetime.date.today().year


def this_week():
    ''' '''
    return int(datetime.date.today().strftime('%W'))


def date_from_week(year=None, week=None):
    '''

    Args:
      year: (Default value = None)
      week: (Default value = None)

    Returns:

    '''
    if year is None:
        year = this_year()
    if week is None:
        week = this_week()
    dstr = '{year}-{week}-1'.format(year=year, week=week)
    return datetime.datetime.strptime(dstr, '%Y-%W-%w')
