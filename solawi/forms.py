import copy
from django import forms
from solawi.models import (
    User,
    OrderBasket,
    WeeklyBasket,
)


class WeeklyBasketForm(forms.Form):
    ''' '''
    prefix = 'weekly'
    contents = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, orderbasket, weeklybasket, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices, initial = self._get_weekly_basket_form_choices(orderbasket,
                                                                weeklybasket)
        self.fields['contents'].choices = choices
        self.fields['contents'].initial = initial

    def _get_weekly_basket_form_choices(self, orderbasket, weeklybasket):
        order_set = weekly_set = weeklybasket.contents.all()
        if orderbasket.edited_weekly_basket:
            order_set = orderbasket.contents.all()
        choices = [(i.id, str(i)) for i in weekly_set]
        initial = [s.id for s in order_set if s in weekly_set]
        return choices, initial


class OrderBasketForm(forms.ModelForm):
    ''' '''
    prefix = 'basket'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.edited_weekly_basket:
            order_set = self.instance.contents.all()
            weekly_set = list(self.instance.user.weeklybasket.contents.all())
            already_removed = [False] * len(weekly_set)
            choices = []
            for item in order_set:
                if item not in weekly_set:
                    choices.append(item)
                elif already_removed[weekly_set.index(item)]:
                    choices.append(item)
                else:
                    already_removed[weekly_set.index(item)] = True
            self.fields['contents'].choices = choices

    class Meta:
        ''' '''
        model = OrderBasket
        fields = ['contents']
