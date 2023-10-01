from django.db import models

from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)
    is_notificated = models.BooleanField(default=True) # defaul True if robot serial exists in db or customer already notificated
    is_abcent = models.BooleanField(default=True)  # True if robot serial exists in db


    def __str__(self):
        return f"#{self.id}"