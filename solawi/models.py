from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Food(models.Model):
    name = models.CharField(max_length=30, unique=True)
    unit = models.CharField(max_length=15,
                            help_text=_('The unit to measure this food in.'
                                        'E.g. kg or L'))
    price = models.FloatField(
        validators=[validators.MinValueValidator(0)],
        help_text=_('The price per unit in Euros.'))
    quantities = models.CharField(
        max_length=250,
        validators=[validators.int_list_validator],
        help_text=_('The possible quantities of this food. Given as list.'
                   'E.g. "1,2,3,4"'))

    def __str__(self):
        return '{} with {}{} costing {} per {}'.format(
            self.name, self.quantities, self.unit, self.price, self.unit)


class Depot(models.Model):
    name = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=30)

    def __str__(self):
        return '{} at {}'.format(self.name, self.location)


class User(AbstractUser):
    isMember = models.BooleanField(_('Make a paying member'), default=True)
    isSupervisor = models.BooleanField(_('Make a Supervisor'), default=False)

    depot = models.ForeignKey('Depot', on_delete=models.CASCADE,
                              related_name='members', blank=True, null=True)
    weeklybasket = models.ForeignKey('WeeklyBasket', on_delete=models.CASCADE,
                                     related_name='members', blank=True, null=True)
    account = models.ManyToManyField('TimedPortions', blank=True, null=True)

    def __str__(self):
        if self.isMember:
            return '{} {}'.format(self.first_name, self.last_name)
        else:
            return '{} {}({})'.format(self.first_name, self.last_name,
                                      self.depot.name)

    def clean(self):
        super().clean()
        if self.isMember:
            if self.depot is None:
                raise ValidationError(_('A Member has to have an Depot.'))
            if self.weeklybasket is None:
                raise ValidationError(_('A Member has to have an weekly basket.'))


class Portion(models.Model):
    food = models.ForeignKey('Food', on_delete=models.CASCADE,
                             related_name='potentials')
    quantity = models.IntegerField()

    def __str__(self):
        return '{}{} of {}'.format(self.quantity, self.food.unit,
                                   self.food.name)


class TimedPortions(models.Model):
    food = models.ForeignKey('Food', on_delete=models.CASCADE,
                             related_name='timedpotentials')
    quantity = models.IntegerField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}{} of {} since {}'.format(self.quantity, self.food.unit,
                                            self.food.name, self.timestamp)


class WeeklyBasket(models.Model):
    name = models.CharField(max_length=50)
    portions = models.ManyToManyField('Portion')

    def __str__(self):
        return '{} containing {}'.format(self.name, self.portions)
