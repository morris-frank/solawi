from django import forms
from solawi.models import (
    OrderBasket,
    WeeklyBasket,
)


class WeeklyBasketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contents'].queryset = kwargs.get('instance').contents

    class Meta:
        model = WeeklyBasket
        fields = ['contents']
        widgets = {'contents': forms.CheckboxSelectMultiple()}


class OrderBasketFrom(forms.ModelForm):
    class Meta:
        model = OrderBasket
        fields = ['contents']
