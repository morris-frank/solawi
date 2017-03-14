from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import portion_account_validate
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    unit = models.CharField(max_length=15,
                            help_text=_('The unit to measure this food in, '
                                        'e.g. kg or L'))
    price = models.FloatField(
        validators=[validators.MinValueValidator(0)],
        help_text=_('The price per unit.'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return _('{n} costing {p} per {u}').format(
            n=self.name, p=self.price, u=self.unit)


class Depot(models.Model):
    name = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('depot')
        verbose_name_plural = _('depots')

    def __str__(self):
        return _('{n} at {l}').format(n=self.name, l=self.location)


class User(AbstractUser):
    is_member = models.BooleanField(_('Make a paying member'), default=True)
    is_supervisor = models.BooleanField(_('Make a depot supervisor'), default=False)

    depot = models.ForeignKey('Depot', on_delete=models.CASCADE,
                              related_name='members', blank=True, null=True)
    weeklybasket = models.ForeignKey('WeeklyBasket', on_delete=models.CASCADE,
                                     related_name='members', blank=True,
                                     null=True)
    account = models.TextField(blank=True, null=True,
                               help_text=_('Containing the JSON array of '
                                           'this users gained potentials'),
                               validators=[portion_account_validate])

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.depot is None:
            return _('{un}: {fn} {ln}').format(
                un=self.username,fn=self.first_name, ln=self.last_name)
        else:
            return _('{un}: {fn} {ln}({dn})').format(
                un=self.username, fn=self.first_name, ln=self.last_name,
                dn=self.depot.name)

    def clean(self):
        super().clean()
        if self.is_supervisor:
            if self.depot is None:
                raise ValidationError(_('A Member has to have an depot.'))
        if self.is_member:
            if self.depot is None:
                raise ValidationError(_('A Member has to have an depot.'))
            if self.weeklybasket is None:
                raise ValidationError(_('A Member has to have an '
                                        'weekly basket.'))


class Portion(models.Model):
    food = models.ForeignKey('Product', on_delete=models.CASCADE,
                             related_name='portions')
    quantity = models.IntegerField()

    class Meta:
        verbose_name = _('portion')
        verbose_name_plural = _('portions')

    def __str__(self):
        return _('{q}{u} of {n}').format(
            q=self.quantity, u=self.food.unit, n=self.food.name)


class WeeklyBasket(models.Model):
    name = models.CharField(max_length=50)
    contents = models.ManyToManyField('Portion')

    class Meta:
        verbose_name = _('weekly basket')
        verbose_name_plural = _('weekly baskets')

    def __str__(self):
        return _('{n}').format(n=self.name)
