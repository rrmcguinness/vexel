import io
import logging
import sys
import threading
from typing import List, Callable

# Try to import Google Cloud Logging
try:
    from google.cloud import logging as cloud_logging
    from google.cloud.logging_v2.handlers import CloudLoggingHandler
    GOOGLE_CLOUD_LOGGING_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_LOGGING_AVAILABLE = False

# Buffer size: 1024k (1MB)
BUFFER_SIZE = 1024 * 1024

class LogStream(io.StringIO):
    """
    A stream that buffers log messages and allows subscribers to receive updates.
    The buffer has a maximum size of BUFFER_SIZE bytes.
    """
    def __init__(self, buffer_size: int = BUFFER_SIZE):
        super().__init__()
        self.buffer_size = buffer_size
        self.subscribers: List[Callable[[str], None]] = []
        self.lock = threading.Lock()

    def write(self, s: str) -> int:
        with self.lock:
            # Check if adding this string would exceed the buffer size
            current_pos = self.tell()
            if current_pos + len(s) > self.buffer_size:
                # Remove content from the beginning to make room
                content = self.getvalue()
                excess = current_pos + len(s) - self.buffer_size
                new_content = content[excess:]
                
                # Reset the buffer and write the truncated content
                self.seek(0)
                self.truncate(0)
                super().write(new_content)
            
            # Write the new content
            result = super().write(s)
            
            # Notify subscribers
            for subscriber in self.subscribers:
                try:
                    subscriber(s)
                except Exception as e:
                    # Don't let subscriber errors affect logging
                    print(f"Error in log subscriber: {e}", file=sys.stderr)
            
            return result

    def subscribe(self, callback: Callable[[str], None]) -> None:
        """
        Add a subscriber that will be called with each new log message.
        
        Args:
            callback: A function that takes a string parameter (the log message)
        """
        with self.lock:
            self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[str], None]) -> None:
        """
        Remove a subscriber.
        
        Args:
            callback: The callback function to remove
        """
        with self.lock:
            if callback in self.subscribers:
                self.subscribers.remove(callback)

class Logger:
    """
    A logger that uses Google Cloud Logging if available, otherwise falls back to local logging.
    Also provides a stream that can be subscribed to for real-time log monitoring.
    """
    def __init__(self, name: str = "sales_team", log_level: int = logging.INFO):
        self.name = name
        self.log_level = log_level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create the log stream with 1024k buffer
        self.log_stream = LogStream()
        
        # Create a handler that writes to the stream
        self.stream_handler = logging.StreamHandler(self.log_stream)
        self.stream_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.stream_handler.setFormatter(formatter)
        self.logger.addHandler(self.stream_handler)
        
        # Set up Google Cloud Logging if available
        self.cloud_client = None
        self.cloud_handler = None
        
        if GOOGLE_CLOUD_LOGGING_AVAILABLE:
            try:
                # Initialize Google Cloud Logging
                self.cloud_client = cloud_logging.Client()
                self.cloud_handler = CloudLoggingHandler(self.cloud_client)
                self.cloud_handler.setLevel(log_level)
                self.logger.addHandler(self.cloud_handler)
                
                # Remove default handlers to avoid duplicate logs
                for handler in self.logger.handlers[:]:
                    if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
                        self.logger.removeHandler(handler)
                
                self.logger.info("Google Cloud Logging initialized successfully")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Google Cloud Logging: {e}")
                self._setup_local_logging()
        else:
            self._setup_local_logging()
    
    def _setup_local_logging(self):
        """Set up local logging as a fallback."""
        # Add a console handler if not already present
        has_console_handler = any(
            isinstance(handler, logging.StreamHandler) and handler.stream in (sys.stdout, sys.stderr)
            for handler in self.logger.handlers
        )
        
        if not has_console_handler:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.logger.info("Local logging initialized as fallback")
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance."""
        return self.logger
    
    def subscribe(self, callback: Callable[[str], None]) -> None:
        """
        Subscribe to the log stream.
        
        Args:
            callback: A function that will be called with each new log message
        """
        self.log_stream.subscribe(callback)
    
    def unsubscribe(self, callback: Callable[[str], None]) -> None:
        """
        Unsubscribe from the log stream.
        
        Args:
            callback: The callback function to remove
        """
        self.log_stream.unsubscribe(callback)
    
    def get_stream_content(self) -> str:
        """Get the current content of the log stream."""
        return self.log_stream.getvalue()

# Create a default logger instance
default_logger = Logger()

# Convenience functions to use the default logger
def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Optional name for the logger. If provided, returns a child logger
             of the default logger with the given name.
    
    Returns:
        A logger instance
    """
    if name:
        return logging.getLogger(f"{default_logger.name}.{name}")
    return default_logger.get_logger()

def subscribe(callback: Callable[[str], None]) -> None:
    """
    Subscribe to the default log stream.
    
    Args:
        callback: A function that will be called with each new log message
    """
    default_logger.subscribe(callback)

def unsubscribe(callback: Callable[[str], None]) -> None:
    """
    Unsubscribe from the default log stream.
    
    Args:
        callback: The callback function to remove
    """
    default_logger.unsubscribe(callback)

def get_stream_content() -> str:
    """Get the current content of the default log stream."""
    return default_logger.get_stream_content()