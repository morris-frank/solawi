from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from .models import Depot, Portion, Product, User, WeeklyBasket


def gemuesekorb(request):
    pass


@login_required
def woche(request, year=None, month=None):
    if year is None:
        year = datetime.today().isocalendar()[0]
    if month is None:
        month = datetime.today().isocalendar()[1]
    user = request.user
    print(user.depot)
    portions_list = Portion.objects.order_by('-quantity')
    context = {'user': user, 'portions_list': portions_list}
    return render(request, 'week.html', context)
