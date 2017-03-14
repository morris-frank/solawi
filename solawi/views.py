from datetime import datetime


def gemuesekorb():
    pass


def woche(year=None, month=None):
    if year is None:
        year = datetime.today().isocalendar()[0]
    if month is None:
        month = datetime.today().isocalendar()[1]
