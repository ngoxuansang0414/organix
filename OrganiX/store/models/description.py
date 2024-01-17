from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .products import Product

class Description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    certification = models.TextField(default='Không rõ')
    origin = models.TextField(default='Không rõ')
    uses = models.TextField(default='Không rõ')
    instructions_for_use = models.TextField(default='Không rõ')
    preserving_instruction = models.TextField(default='Không rõ')
    expiry = models.TextField(default='Không rõ')

    @receiver(post_save, sender=Product)
    def create_description(sender, instance, created, **kwargs):
        if created:
            Description.objects.create(product = instance)

    def __str__(self):
        return self.product.name