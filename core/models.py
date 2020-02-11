from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('core:list_of_products_by_category',args=[self.slug])

    def __str__(self):
        return self.name

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=50)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(null=True)
    published_on = models.DateTimeField(auto_now_add=True)
