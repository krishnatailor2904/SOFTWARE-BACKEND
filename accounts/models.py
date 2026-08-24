from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Har user (shop owner) ka ek profile hota hai jisme uski shop/brand ka
    naam save hota hai. Login karne ke baad ye naam upar (header me) dikhta hai.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    shop_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.shop_name
