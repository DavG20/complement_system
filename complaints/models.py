from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("solved", "Solved"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )  # Set default to 'pending'
    answereddby = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="approved_by",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
