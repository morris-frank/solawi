import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from solawi.validators import portion_account_validate
from django.utils.translation import ugettext_lazy as _
import json
from solawi import utils


class User(AbstractUser):
    is_member = models.BooleanField(_('Make a paying member'), default=True)
    is_supervisor = models.BooleanField(_('Make a depot supervisor'), default=False)

    depot = models.ForeignKey('Depot', on_delete=models.CASCADE,
                              related_name='members', blank=True, null=True)
    weeklybasket = models.ForeignKey('WeeklyBasket', on_delete=models.CASCADE,
                                     related_name='members', blank=True,
                                     null=True)
    assets = models.IntegerField(null=True, blank=True, default='',
                                 validators=[validators.MinValueValidator(0)])
    account = models.TextField(null=True, blank=True, default=0,
                               help_text=_('Containing the JSON array of '
                                           'this users gained potentials'),
                               validators=[portion_account_validate])

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.first_name == '' and self.last_name == '':
            name = self.username
        else:
            name = self.first_name + ' ' + self.last_name
        if self.depot is None:
            return _('{name}').format(name=name)
        else:
            return _('{name} ({depot})').format(name=name,
                                                depot=self.depot.name)

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

    def save(self, *args, **kwargs):
        if self.account:
            self.assets = 0
            this_week = utils.date_from_week()
            valid_days = settings.WEEKS_TO_SAVE_ACCOUNTS * 7
            for (year, week, asset) in json.loads(self.account):
                date_delta = (this_week - utils.date_from_week(week, year)).days
                if date_delta <= valid_days:
                    self.assets += asset
        super().save(*args, **kwargs)


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
        return self.name


class Portion(models.Model):
    food = models.ForeignKey('Product', on_delete=models.CASCADE,
                             related_name='portions')
    quantity = models.IntegerField()
    price = models.FloatField(
        validators=[validators.MinValueValidator(0)],
        help_text=_('The price of this Portion.'),
        default=0)
    # quantity = models.FloatField(
    #     validators=[validators.MinValueValidator(0)],
    #     help_text=_('The quantity of this Portion.'))

    class Meta:
        verbose_name = _('portion')
        verbose_name_plural = _('portions')

    def __str__(self):
        return _('{quantity}{unit} of {food}').format(
            quantity=self.quantity, unit=self.food.unit, food=self.food)

    def get_price(self):
        return self.quantity * self.food.price

    def save(self, *args, **kwargs):
        self.price = self.get_price()
        super().save(*args, **kwargs)


class Depot(models.Model):
    name = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('depot')
        verbose_name_plural = _('depots')

    def __str__(self):
        return _('{name} at {location}').format(name=self.name,
                                                location=self.location)


class WeeklyBasket(models.Model):
    name = models.CharField(max_length=50)
    contents = models.ManyToManyField('Portion')

    class Meta:
        verbose_name = _('weekly basket')
        verbose_name_plural = _('weekly baskets')

    def __str__(self):
        cstr = ', '.join([str(i) for i in self.contents.all()])
        return _('{name}: {contents}').format(name=self.name,
                                              contents=cstr)


class OrderBasket(models.Model):
    week = models.DateField()
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             related_name='orders')
    contents = models.ManyToManyField('Portion')

    class Meta:
        verbose_name = _('order basket')
        verbose_name_plural = _('order baskets')
        unique_together = ('week', 'user')

    def clean(self):
        super().clean()
        week = self.week - datetime.timedelta(self.week.weekday())
        existingOrders = OrderBasket.objects.filter(user=self.user, week=week)
        if len(existingOrders) > 0:
            raise ValidationError(_('There is already an order for this week.'
                                    ' Update that instead.'))

    def save(self, *args, **kwargs):
        # Set every date on Monday!
        self.week -= datetime.timedelta(self.week.weekday())
        super().save(*args, **kwargs)

    def __str__(self):
        ostr = ', '.join([str(i) for i in self.contents.all()])
        week = self.week.strftime('%W')
        year = self.week.year
        return _('{year}-{week} by {user}: {contents}').format(
            year=year, week=week, user=self.user, contents=ostr)
