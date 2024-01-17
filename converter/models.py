from django.db import models
from django.utils.text import slugify


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    base = models.CharField(max_length=3, default='EUR')
    exchange_rate = models.DecimalField(max_digits=30, decimal_places=15)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
