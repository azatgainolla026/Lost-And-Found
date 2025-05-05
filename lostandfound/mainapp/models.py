from datetime import date
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    class StatusChoices(models.TextChoices):
        CLAIMED = 'Claimed'
        UNCLAIMED = 'Unclaimed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='found_items')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_found = models.DateField(auto_now_add=True)
    item_status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.UNCLAIMED)
    location = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, through="ItemTag")
    image = models.ImageField(upload_to="images/", null=True,)

    @property
    def days_since_found(self):
        return (date.today() - self.date_found).days

    @property
    def claimed_status(self):
        return self.item_status == self.StatusChoices.CLAIMED

    def __str__(self):
        return f"Found: {self.name} by {self.user.username}"

class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.name} - {self.tag.name}"


class ClaimRequest(models.Model):
    found_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claim_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claim_requests_received')
    contact_info = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Claim by {self.claimant.username} on {self.found_item.name}"
