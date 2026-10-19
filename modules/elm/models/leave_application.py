from django.db import models
from datetime import datetime
from .leave_types import LeaveType, LeaveBalance

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RECOMMENDED', 'Recommended'),
        ('NOT_RECOMMENDED', 'Not Recommended'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
        ('CANCELLED', 'Cancelled'),
    ]

    user_id = models.IntegerField()
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    purpose = models.TextField()
    station_leave_details = models.JSONField(default=dict, blank=True)
    substitute_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING', choices=STATUS_CHOICES)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    decision_maker_id = models.IntegerField(null=True, blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Leave Application"
        db_table = "elm_leave_application"

    def __str__(self):
        return f"LeaveApp-{self.id} (User {self.user_id})"
