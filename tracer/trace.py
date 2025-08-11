from typing import Optional, Dict, Any, Iterator, ContextManager
from contextlib import contextmanager
from common.py.libs.logging.logging import get_logger

# Try to import OpenTelemetry and Google Cloud Trace
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
    from opentelemetry.baggage.propagation import W3CBaggagePropagator
    from opentelemetry import baggage
    from opentelemetry.trace.span import Span
    OPEN_TELEMETRY_AVAILABLE = True
except ImportError:
    OPEN_TELEMETRY_AVAILABLE = False

logger = get_logger("trace")

class Tracer:
    """
    A singleton utility class for OpenTelemetry tracing with Google Cloud Trace.
    Provides methods for starting and stopping spans with baggage.
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs) -> 'Tracer':
        """
        Create a singleton instance of the Tracer class.

        Returns:
            The singleton Tracer instance
        """
        if cls._instance is None:
            cls._instance = super(Tracer, cls).__new__(cls)
        return cls._instance

    def __init__(self, service_name: str = "gas-service"):
        """
        Initialize the tracer with OpenTelemetry and Google Cloud Trace.
        This will only run once for the singleton instance.

        Args:
            service_name: The name of the service for tracing
        """
        # Skip initialization if already initialized
        if Tracer._initialized:
            return

        self.service_name = service_name
        self.tracer = None

        if OPEN_TELEMETRY_AVAILABLE:
            try:
                # Initialize OpenTelemetry tracer provider
                provider = TracerProvider()
                trace.set_tracer_provider(provider)

                # Set up Google Cloud Trace exporter
                cloud_trace_exporter = CloudTraceSpanExporter()
                processor = BatchSpanProcessor(cloud_trace_exporter)
                provider.add_span_processor(processor)

                # Get a tracer
                self.tracer = trace.get_tracer(self.service_name)

                logger.info("OpenTelemetry with Google Cloud Trace initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenTelemetry with Google Cloud Trace: {e}")
                self._setup_noop_tracer()
        else:
            logger.warning("OpenTelemetry not available, using no-op tracer")
            self._setup_noop_tracer()

        Tracer._initialized = True

    def _setup_noop_tracer(self):
        """Set up a no-op tracer as a fallback."""
        self.tracer = trace.get_tracer(self.service_name)

    @contextmanager
    def start_span(self, name: str, attributes: Optional[Dict[str, Any]] = None, 
                  baggage_items: Optional[Dict[str, str]] = None) -> Iterator[Span]:
        """
        Start a new span with the given name, attributes, and baggage items.

        Args:
            name: The name of the span
            attributes: Optional attributes to add to the span
            baggage_items: Optional baggage items to add to the span

        Returns:
            A context manager that yields the span
        """
        if not self.tracer:
            # Return a dummy context manager if tracer is not available
            @contextmanager
            def dummy_context():
                yield None
            return dummy_context()

        # Set baggage items if provided
        if baggage_items:
            for key, value in baggage_items.items():
                baggage.set_baggage(key, value)

        # Start the span with attributes
        span_attributes = attributes or {}
        with self.tracer.start_as_current_span(name, attributes=span_attributes) as span:
            try:
                yield span
            finally:
                # Clear baggage items when span ends
                if baggage_items:
                    for key in baggage_items:
                        baggage.remove_baggage(key)

    def get_current_span(self) -> Optional[Span]:
        """Get the current active span."""
        if not self.tracer:
            return None
        return trace.get_current_span()

    @staticmethod
    def add_event_to_span(span: Span, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an event to the specified span.

        Args:
            span: The span to add the event to
            name: The name of the event
            attributes: Optional attributes for the event
        """
        if span:
            span.add_event(name, attributes=attributes or {})

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an event to the current span.

        Args:
            name: The name of the event
            attributes: Optional attributes for the event
        """
        span = self.get_current_span()
        self.add_event_to_span(span, name, attributes)

    @staticmethod
    def set_attribute_on_span(span: Span, key: str, value: Any) -> None:
        """
        Set an attribute on the specified span.

        Args:
            span: The span to set the attribute on
            key: The attribute key
            value: The attribute value
        """
        if span:
            span.set_attribute(key, value)

    def set_attribute(self, key: str, value: Any) -> None:
        """
        Set an attribute on the current span.

        Args:
            key: The attribute key
            value: The attribute value
        """
        span = self.get_current_span()
        self.set_attribute_on_span(span, key, value)

    @staticmethod
    def set_baggage(key: str, value: str) -> None:
        """
        Set a baggage item.

        Args:
            key: The baggage key
            value: The baggage value
        """
        if OPEN_TELEMETRY_AVAILABLE:
            baggage.set_baggage(key, value)

    @staticmethod
    def get_baggage(key: str) -> Optional[str]:
        """
        Get a baggage item.

        Args:
            key: The baggage key

        Returns:
            The baggage value or None if not found
        """
        if OPEN_TELEMETRY_AVAILABLE:
            return baggage.get_baggage(key)
        return None

    @staticmethod
    def remove_baggage(key: str) -> None:
        """
        Remove a baggage item.

        Args:
            key: The baggage key to remove
        """
        if OPEN_TELEMETRY_AVAILABLE:
            baggage.remove_baggage(key)

# Convenience functions to use the singleton tracer instance
def start_span(name: str, attributes: Optional[Dict[str, Any]] = None, 
               baggage_items: Optional[Dict[str, str]] = None) -> ContextManager[Optional[Span]]:
    """
    Start a new span with the given name, attributes, and baggage items.

    Args:
        name: The name of the span
        attributes: Optional attributes to add to the span
        baggage_items: Optional baggage items to add to the span

    Returns:
        A context manager that yields the span
    """
    return Tracer().start_span(name, attributes, baggage_items)

def get_current_span() -> Optional[Span]:
    """Get the current active span."""
    return Tracer().get_current_span()

def add_event(name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
    """
    Add an event to the current span.

    Args:
        name: The name of the event
        attributes: Optional attributes for the event
    """
    Tracer().add_event(name, attributes)

def add_event_to_span(span: Span, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
    """
    Add an event to the specified span.

    Args:
        span: The span to add the event to
        name: The name of the event
        attributes: Optional attributes for the event
    """
    Tracer.add_event_to_span(span, name, attributes)

def set_attribute(key: str, value: Any) -> None:
    """
    Set an attribute on the current span.

    Args:
        key: The attribute key
        value: The attribute value
    """
    Tracer().set_attribute(key, value)

def set_attribute_on_span(span: Span, key: str, value: Any) -> None:
    """
    Set an attribute on the specified span.

    Args:
        span: The span to set the attribute on
        key: The attribute key
        value: The attribute value
    """
    Tracer.set_attribute_on_span(span, key, value)

def set_baggage(key: str, value: str) -> None:
    """
    Set a baggage item.

    Args:
        key: The baggage key
        value: The baggage value
    """
    Tracer.set_baggage(key, value)

def get_baggage(key: str) -> Optional[str]:
    """
    Get a baggage item.

    Args:
        key: The baggage key

    Returns:
        The baggage value or None if not found
    """
    return Tracer.get_baggage(key)

def remove_baggage(key: str) -> None:
    """
    Remove a baggage item.

    Args:
        key: The baggage key to remove
    """
    Tracer.remove_baggage(key)
