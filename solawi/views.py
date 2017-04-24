import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render,
    )
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views import generic
from solawi import forms
from solawi.models import (
    Depot,
    OrderBasket,
    OrderBasketProduct,
    Portion,
    Product,
    User,
    WeeklyBasket,
    )
from solawi import utils
from solawi.utils import view_property


@method_decorator(login_required, name='dispatch')
class BaseMemberView(generic.TemplateView):
    ''' '''
    template_name = 'base_user.html'

    @view_property
    def user(self):
        ''' '''
        return self.request.user

    @view_property
    def controls(self):
        ''' '''
        controls = {
            'depot': '/depot/{depot}/'.format(depot=self.user.depot.id)
            }
        return controls


@method_decorator(login_required, name='dispatch')
class WeekView(BaseMemberView):
    ''' '''
    template_name = 'week.html'

    def post(self, request, *args, **kwargs):
        '''

        Args:
          request:
          *args:
          **kwargs:

        Returns:

        '''
        weekly_basket_form = forms.WeeklyBasketForm(
            data=request.POST, orderbasket=self.orders,
            weeklybasket=self.user.weeklybasket)
        if weekly_basket_form.is_valid():
            print(weekly_basket_form.__dict__)
            # weekly_basket_form.save()

        order_basket_form = forms.OrderBasketForm(
            request.POST, instance=self.orders)
        if order_basket_form.is_valid():
            print('is valide')
            # order_basket_form.save()
            order_basket_mod = order_basket_form.save(commit=False)
            order_basket_mod.save()
            # OrderBasketProduct.objects.filter(basket=order_basket_mod).delete()
            for portion in order_basket_form.cleaned_data.get('contents'):
                order_basket_product = OrderBasketProduct.objects.filter(basket=order_basket_mod)
                if order_basket_product:
                    order_basket_product = order_basket_product[0]
                    order_basket_product.count += 1
                else:
                    order_basket_product = OrderBasketProduct(
                        basket=order_basket_mod, portion=portion, count=1)
                order_basket_product.save()
        return self.get(request, *args, **kwargs)

    @view_property
    def week_start(self):
        ''' '''
        year = self.kwargs.get('year', None)
        week = self.kwargs.get('week', None)
        return utils.date_from_week(year, week)

    @view_property
    def week_end(self):
        ''' '''
        return self.week_start + datetime.timedelta(6)

    @view_property
    def portions_list(self):
        ''' '''
        return Portion.objects.order_by('-quantity')

    @view_property
    def orders(self):
        ''' '''
        orders = self.user.orders.filter(week=self.week_start)
        if orders:
            return orders[0]
        else:
            orders = OrderBasket(week=self.week_start, user=self.user)
            orders.save()
            return orders

    @view_property
    def weekly_basket_form(self):
        ''' '''
        # if self.user.weeklybasket:
            # return forms.WeeklyBasketForm(instance=self.user.weeklybasket)
        return forms.WeeklyBasketForm(orderbasket=self.orders,
                                      weeklybasket=self.user.weeklybasket)

    @view_property
    def order_basket_form(self):
        ''' '''
        return forms.OrderBasketForm(instance=self.orders)

    @view_property
    def controls(self):
        ''' '''
        controls = super().controls
        for name, multi in [('next_week', 1), ('prev_week', -1)]:
            week = self.week_start + multi * datetime.timedelta(7)
            controls[name] = week.strftime('/woche/%Y/%W')
        return controls


@method_decorator(login_required, name='dispatch')
class DepotView(BaseMemberView):
    ''' '''
    template_name = 'depot.html'

    @view_property
    def depot(self):
        ''' '''
        self.depot_id = self.kwargs.get('depot_id', None)
        return get_object_or_404(Depot, id=self.depot_id)

    @view_property
    def members(self):
        ''' '''
        return self.depot.members.all()
