import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from solawi import forms
from solawi.models import (
    Depot,
    OrderBasket,
    Portion,
    Product,
    User,
    WeeklyBasket,
)
from solawi import utils


def gemuesekorb(request):
    pass


@login_required
def woche(request, year=None, week=None):
    date = utils.date_from_week(year, week)
    user = request.user

    weeklybasketform = None
    if user.weeklybasket:
        weeklybasketform = forms.WeeklyBasketForm(instance=user.weeklybasket)

    orders = user.orders.filter(week=date)
    orderbasketform = None
    if orders:
        orders = orders[0]
        orderbasketform = forms.OrderBasketFrom(instance=orders)

    portions_list = Portion.objects.order_by('-quantity')
    context = {'user': user,
               'orders': orders,
               'weekly_basket_form': weeklybasketform,
               'order_basket_form': orderbasketform,
               'portions_list': portions_list,
               'controls': {'next_week': date + datetime.timedelta(7),
                            'prev_week': date - datetime.timedelta(7)}}
    return render(request, 'week.html', context)
