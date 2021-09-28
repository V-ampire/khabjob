"""App loggers."""
import logging
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from queue import Queue


DEFAULT_LOGFILE_SIZE = 2000
DEFAULT_BACKUP_COUNT = 20


class QueueFileHandler(QueueHandler):
    """Logger to run rotating file handler in separate thread."""

    def __init__(self, filename, **kwargs):
        """
        Initialization.
        
        Create queue and start listener.
        """
        self.queue = Queue(-1)
        super().__init__(self.queue)

        maxBytes = kwargs.pop('maxBytes', DEFAULT_LOGFILE_SIZE)
        backupCount = kwargs.pop('backupCount', DEFAULT_BACKUP_COUNT)
        
        self.handler = RotatingFileHandler(
            filename, 
            maxBytes=maxBytes, 
            backupCount=backupCount,
            **kwargs
        )
        self.listener = QueueListener(self.queue, self.handler)
        self.listener.start()

    def setFormatter(self, formatter: logging.Formatter) -> None:
        """
        Set formatter to handler.
        
        :param formatter: Formatter instance.
        """
        self.handler.setFormatter(formatter)

    def close(self) -> None:
        """Wait till all records will be processed then stop listener."""
        self.listener.stop()
        super().close()
