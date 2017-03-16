import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from solawi.models import Depot, Portion, Product, User, WeeklyBasket, OrderBasket
from solawi import utils


def gemuesekorb(request):
    pass


@login_required
def woche(request, year=None, week=None):
    date = utils.date_from_week(year, week)
    user = request.user
    try:
        orders = user.orders.get(week=date)
    except OrderBasket.DoesNotExist:
        orders = None
    portions_list = Portion.objects.order_by('-quantity')
    context = {'user': user,
               'orders': orders,
               'portions_list': portions_list,
               'controls': {'next_week': date + datetime.timedelta(7),
                            'prev_week': date - datetime.timedelta(7)}}
    return render(request, 'week.html', context)
