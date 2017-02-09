from django.db import models


class Depot(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)


class User(models.Model):
    first_name = models.CharField("The persons first name", max_length=30)
    last_name = models.CharField("The persons last name", max_length=30)
    mail = models.EmailField("The persons E-Mail address")


class Member(User):
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)


class Depotbesteller(Member):
    pass


class PackSize(models.Model):
    quantity = models.IntegerField()
    unit = models.CharField(max_length=15)


class Food(models.Model):
    name = models.CharField(max_length=30)
    packsizes = models.ManyToManyField(
        PackSize,
        through='PackSizeRelation',
        through_fields=('food', 'packsize'),
        )
    foodexchanges = models.ManyToManyField(
        FoodExchange,
        through='FoodExchangeRelation',
        through_fields=('food', 'foodexchange'),
        )


class PackSizeRelation(models.Model):
    packsize = models.ForeignKey(PackSize, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class FoodExchange(models.Model):
    sourcesize = models.ForeignKey(PackSize, on_delete=models.CASCADE)
    target = models.ForeignKey(Food, on_delete=models.CASCADE)
    targetsize = models.ForeignKey(PackSize, on_delete=models.CASCADE)


class FoodExchangeRelation(models.Model):
    foodexchange = models.ForeignKey(FoodExchange, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
