from django.db import models


class Booking(models.Model):
    """
    (Optional) Booking model — only include this if not already defined elsewhere.
    """
    user_email = models.EmailField()
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    booking_reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.destination}"


class Payment(models.Model):
    """
    Stores payment information related to a booking via Chapa.
    """
    booking_reference = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"

    class Meta:
        ordering = ['-created_at']
