from django.db import models
from django.contrib.auth.models import User
from Items.models import Item

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jeweler_transactions')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='jeweler_transactions')
    transaction_type = models.CharField(max_length=10)
    price = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.transaction_type})"
