from django.conf import settings
from django.db import models
from django.utils import timezone 


class Bill(models.Model):
    """
    Ek bill = ek customer ki entry.
    owner = kis shop-account ne ye bill banaya (login wale user se link).
    Isi wajah se har shop sirf apna data dekhega, doosre ka nahi.
    bill_no khud se generate hota hai (auto-increment jaisa) lekin
    tum chaho to edit bhi kar sakte ho.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bills')
    bill_no = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, default='')
    bill_date = models.DateField(default=timezone.localdate)
    delivery_date = models.DateField(null=True, blank=True)
    cloth_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stitching_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.TextField(blank=True, default='')

    # Order status - ye wahi checkbox wala feature hai
    shirt_ready = models.BooleanField(default=False)
    pant_ready = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'bill_no')

    @property
    def total(self):
        return self.cloth_price + self.stitching_price

    def __str__(self):
        return f"{self.bill_no} - {self.name}"


class Measurement(models.Model):
    """
    Har bill ki apni ek measurement sheet hoti hai (Shirt + Pant).
    OneToOne isliye ki ek bill ki sirf ek measurement entry ho.
    """
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name='measurement')

    # ---- SHIRT measurements ----
    shirt_length = models.CharField(max_length=20, blank=True, default='')
    shirt_chest = models.CharField(max_length=20, blank=True, default='')
    shirt_stomach = models.CharField(max_length=20, blank=True, default='')
    shirt_sleeve = models.CharField(max_length=20, blank=True, default='')
    shirt_shoulder = models.CharField(max_length=20, blank=True, default='')
    shirt_collar = models.CharField(max_length=20, blank=True, default='')

    # ---- PANT measurements ----
    pant_length = models.CharField(max_length=20, blank=True, default='')
    pant_waist = models.CharField(max_length=20, blank=True, default='')
    pant_hip = models.CharField(max_length=20, blank=True, default='')
    pant_bottom = models.CharField(max_length=20, blank=True, default='')
    pant_thigh = models.CharField(max_length=20, blank=True, default='')
    pant_seat_langot = models.CharField(max_length=20, blank=True, default='')

    notes = models.TextField(blank=True, default='')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Measurement for {self.bill.bill_no}"
