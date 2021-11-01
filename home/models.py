from django.db import models
from django.db.models.base import Model

# Create your models here.
class Men_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Men_product_category(models.Model):
    category = models.ForeignKey(Men_category, on_delete=models.CASCADE, default=False, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Men_Product(models.Model):
    image = models.ImageField(upload_to='pics', null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Men_product_category, on_delete=models.CASCADE, default=False, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    # is_published = models.BooleanField(default=True)
    # created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

class Women_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Women_product_category(models.Model):
    category = models.ForeignKey(Women_category, on_delete=models.CASCADE, default=False, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Women_Product(models.Model):
    image = models.ImageField(upload_to='pics', null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Women_product_category, on_delete=models.CASCADE, default=False, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    # is_published = models.BooleanField(default=True)
    # created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

class Kid_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kid_product_category(models.Model):
    category = models.ForeignKey(Kid_category, on_delete=models.CASCADE, default=False, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kid_Product(models.Model):
    image = models.ImageField(upload_to='pics', null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Kid_product_category, on_delete=models.CASCADE, default=False, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
       