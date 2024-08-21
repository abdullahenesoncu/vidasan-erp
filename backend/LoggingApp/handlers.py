import logging

class DatabaseLogHandler(logging.Handler):
    """
    Custom logging handler that writes logs to the database using the LogEntry model.
    """
    def emit(self, record):
        from .models import LogEntry
        try:
            # Create a new LogEntry object and save it to the database
            LogEntry.objects.create(
                level=record.levelname,
                message=record.getMessage(),
                logger_name=record.name,
                file_name=record.pathname,
                line_number=record.lineno,
                function_name=record.funcName,
            )
        except Exception:
            # In case of an error (e.g., database error), fail silently
            pass
