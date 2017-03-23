import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
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
from solawi.utils import view_property


@method_decorator(login_required, name='dispatch')
class BaseMemberView(generic.TemplateView):
    template_name = 'base_user.html'

    @view_property
    def user(self):
        return self.request.user

    @view_property
    def controls(self):
        return {}


@method_decorator(login_required, name='dispatch')
class Woche(BaseMemberView):
    template_name = 'week.html'

    @view_property
    def week_start(self):
        year = self.kwargs.get('year', None)
        week = self.kwargs.get('week', None)
        return utils.date_from_week(year, week)

    @view_property
    def week_end(self):
        return self.week_start + datetime.timedelta(6)

    @view_property
    def portions_list(self):
        return Portion.objects.order_by('-quantity')

    @view_property
    def weekly_basket_form(self):
        if self.user.weeklybasket:
            return forms.WeeklyBasketForm(instance=self.user.weeklybasket)

    @view_property
    def orders(self):
        orders = self.user.orders.filter(week=self.week_start)
        if orders:
            return orders[0]

    @view_property
    def order_basket_form(self):
        return forms.OrderBasketFrom(instance=self.orders)

    @view_property
    def controls(self):
        controls = super().controls
        controls['next_week'] = (self.week_start + datetime.timedelta(7)).strftime("/woche/%Y/%W")
        controls['prev_week'] = (self.week_start - datetime.timedelta(7)).strftime("/woche/%Y/%W")
        return controls
