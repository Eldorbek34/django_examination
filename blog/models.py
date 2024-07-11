from django.db import models

class Company(models.Model):
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    @property
    def products_count(self):
        return self.products.count()

class Product(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if self.product.quantity < self.quantity:
            raise ValueError('Not enough quantity in stock')
        self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
