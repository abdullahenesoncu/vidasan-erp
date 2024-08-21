from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'message', 'file_name', 'line_number')
    search_fields = ('message',)
    list_filter = ('level', 'timestamp')