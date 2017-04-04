from django import forms
from solawi.models import (
    User,
    OrderBasket,
    WeeklyBasket,
)


class WeeklyBasketForm(forms.Form):
    ''' '''
    contents = forms.MultipleChoiceField()

    def __init__(self, orderbasket, weeklybasket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = weeklybasket.contents.all()
        if orderbasket.edited_weekly_basket:
            subset = orderbasket.contents.all() & queryset
        else:
            subset = queryset
        choices = [(i.id, str(i)) for i in queryset]
        initial = list()
        for s in subset:
            if s in queryset:
                initial.append(s.id)
        self.prefix = 'weekly'
        self.fields['contents'] = forms.MultipleChoiceField(
            choices=choices,
            widget = forms.CheckboxSelectMultiple(),
            initial=initial
            )
        print(self.fields['contents'].__dict__)

    class Meta:
        ''' '''
        model = OrderBasket
        fields = ['edited_weekly_basket', 'contents']
        widgets = {'contents': forms.CheckboxSelectMultiple()}


class OrderBasketFrom(forms.ModelForm):
    ''' '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'basket'

    class Meta:
        ''' '''
        model = OrderBasket
        fields = ['contents']
