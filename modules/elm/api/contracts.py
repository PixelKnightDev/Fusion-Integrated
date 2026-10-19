from django.db import models
from modules.elm.models.leave_types import LeaveType, LeaveBalance
from modules.elm.models.leave_application import LeaveApplication


class LeaveApplicationSerializer(models.Model):
    # Not a model, but a serializer concept.
    # I'll use DRF-like structure in the API directory if needed or just define classes.
    pass

# Using a more standard approach for the prompt:
# Since I need to implement the API (serializers, views, urls), 
# I'll create the directory structure and then put the files.
