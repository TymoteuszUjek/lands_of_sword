from django.db import models
from django.contrib.auth.models import User
from Items.models import Item
#from Inventory.models import InventoryItem

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blacksmith_transactions')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='blacksmith_transactions')
    #inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  # "buy" or "sell"
    price = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_count = models.IntegerField(default=0)  # Dodaj to pole

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.transaction_type})"
