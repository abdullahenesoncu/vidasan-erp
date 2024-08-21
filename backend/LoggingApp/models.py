from django.db import models
from django.utils import timezone
from backend.models import BaseModel

class LogEntry( BaseModel ):
    level = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    logger_name = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    line_number = models.IntegerField(null=True, blank=True)
    function_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.timestamp} - {self.level} - {self.message[:50]}...'
