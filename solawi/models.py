from django.db import models


class Portion(models.Model):
    quantity = models.IntegerField()
    unit = models.CharField(max_length=15)
    food = models.ForeignKey('Food', on_delete=models.CASCADE,
                             related_name='portions')

    def __str__(self):
        return '{}{} of {}'.format(self.quantity, self.unit,
                                   self.food.name)


class Food(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)


class Swap(models.Model):
    source = models.ForeignKey('Portion', on_delete=models.CASCADE,
                               related_name='swpas')
    target = models.ForeignKey('Portion', on_delete=models.CASCADE)

    def __str__(self):
        return '{}{} {} for {}{} {}'.format(
            self.target.quantity, self.target.unit, self.target.food,
            self.source.quantity, self.source.unit, self.source.food,)


class Depot(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)

    def __str__(self):
        return '{} at {}'.format(self.name, self.location)


class User(models.Model):
    first_name = models.CharField('The persons first name', max_length=30)
    last_name = models.CharField('The persons last name', max_length=30)
    mail = models.EmailField('The persons E-Mail address')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Member(User):
    depot = models.ForeignKey('Depot', on_delete=models.CASCADE,
                              related_name='members')

    def __str__(self):
        return '{} {}({})'.format(self.first_name, self.last_name,
                                  self.depot.name)


class DepotHead(Member):
    def __str__(self):
        return '{} {}({})'.format(self.first_name, self.last_name,
                                  self.depot.name)


class Potential(models.Model):
    portion = models.ForeignKey('Portion', on_delete=models.CASCADE,
                                 related_name='potentials')
    member = models.ForeignKey('Member', on_delete=models.CASCADE,
                               related_name='potentials')

    def __str__(self):
        return '{} {} has {}{} {}'.format(
            self.member.first_name, self.member.last_name,
            self.portion.quantity, self.portion.unit,
            self.portion.food.name)


class TimedPotential(models.Model):
    portion = models.ForeignKey('Portion', on_delete=models.CASCADE,
                                 related_name='timedpotentials')
    member = models.ForeignKey('Member', on_delete=models.CASCADE,
                               related_name='timedpotentials')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} {} has {}{} {} since {}'.format(
            self.member.first_name, self.member.last_name,
            self.portion.quantity, self.portion.unit, self.portion.food.name,
            self.timestamp)
