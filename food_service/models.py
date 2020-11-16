from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Food(models.Model):
    seller = models.ForeignKey(verbose_name='Seller', to=User, on_delete=models.CASCADE, limit_choices_to={
        'groups__name': 'seller',
    })
    name = models.CharField(verbose_name='Name', max_length=31)
    price = models.IntegerField(verbose_name='Price ($)')
    image = models.ImageField(verbose_name='Food Image', upload_to='media/food/')
    category = models.CharField(verbose_name='Category', max_length=1, choices=(
        ('N', 'Non-Veg'), ('V', 'Veg')
    ), default='V')
    discount = models.FloatField(verbose_name='Discount (%)', default=0.00)
    tax = models.FloatField(verbose_name='Tax (%)', default=0.00)
    labels = models.CharField(verbose_name='Labels', max_length=255)
    quantity_to_be_prepared = models.IntegerField(verbose_name='Quantity to be prepared', default=0)

    def __str__(self):
        return f'{self.seller.username} --> {self.name}'

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Food'


class OrderQuantity(models.Model):
    food = models.ForeignKey(verbose_name='Food', to=Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Quantity', default=1)
    delivered = models.BooleanField(verbose_name='Delivered', default=False)

    def __str__(self):
        return f'Food -> {self.food.name} Quantity -> {self.quantity}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        if self.delivered:
            self.food.quantity_to_be_prepared -= self.quantity
        else:
            self.food.quantity_to_be_prepared += self.quantity
        self.food.save()

    class Meta:
        verbose_name = 'Order Quantity'
        verbose_name_plural = 'Order Quantity'


class Order(models.Model):
    buyer = models.ForeignKey(
        verbose_name='Buyer', to=User, on_delete=models.CASCADE, limit_choices_to={
            'groups__name': 'buyer'
        }
    )
    components = models.ManyToManyField(verbose_name='Component', to=OrderQuantity)
    delivered = models.BooleanField(verbose_name='Delivered', default=False)

    def __str__(self):
        return f'{self.id} --> {self.buyer}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        for order_quantity in self.components.all():
            order_quantity.delivered = self.delivered
            order_quantity.save()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
