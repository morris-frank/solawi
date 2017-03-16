from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from solawi.models import Depot, Portion, Product, User, WeeklyBasket
from solawi import utils


def gemuesekorb(request):
    pass


@login_required
def woche(request, year=None, week=None):
    if year is None:
        year = utils.this_year()
    if week is None:
        week = utils.this_week()
    user = request.user
    portions_list = Portion.objects.order_by('-quantity')
    context = {'user': user, 'portions_list': portions_list}
    return render(request, 'week.html', context)
