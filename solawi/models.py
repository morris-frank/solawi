from django.core import validators
from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=30, unique=True)
    unit = models.CharField(max_length=15)
    price = models.FloatField(validators=validators.MinValueValidator(0))
    quantities = models.CharField(max_length=250,
                                  validators=[validators.int_list_validator])

    def __str__(self):
        return '{} with {}{} costing {} per {}'.format(
            self.name, self.quantities, self.unit, self.price, self.unit)


class Depot(models.Model):
    name = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=30)

    def __str__(self):
        return '{} at {}'.format(self.name, self.location)


class User(models.Model):
    first_name = models.CharField('The persons first name', max_length=30)
    last_name = models.CharField('The persons last name', max_length=30)
    mail = models.EmailField('The persons E-Mail address', unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Member(User):
    depot = models.ForeignKey('Depot', on_delete=models.CASCADE,
                              related_name='members')
    weeklybasket = models.ForeignKey('WeeklyBasket', on_delete=models.CASCADE,
                                     related_name='members')
    account = models.ManyToManyField('TimedPortions')
    isSupervisor = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}({})'.format(self.first_name, self.last_name,
                                  self.depot.name)


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
