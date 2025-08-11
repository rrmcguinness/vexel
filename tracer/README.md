# Google Trace

## Tracer

The `trace.py` module provides a tracing utility that integrates with OpenTelemetry and Google Cloud Trace. It includes:

- A `Tracer` class for initializing OpenTelemetry with Google Cloud Trace
- Methods for starting and stopping spans with baggage
- Convenience functions for using the default tracer

### Usage

```python
import time
from internal.python.gpc_trace.trace import start_span, set_attribute, add_event, get_baggage

# Start a span with a name and some attributes
with start_span("operation_name",
                attributes={"operation.name": "example", "operation.type": "demo"},
                baggage_items={"context.id": "12345"}) as span:
    # Add an event to the span
    add_event("operation_started", {"timestamp": time.time()})

    # Do some work
    # ...

    # Set an attribute on the span
    set_attribute("operation.result", "success")

    # Get baggage item
    context_id = get_baggage("context.id")

    # Add another event
    add_event("operation_completed", {"timestamp": time.time()})
```

### Nested Spans

```python
from internal.python.gpc_trace.trace import start_span, add_event

# Start a parent span
with start_span("parent_operation") as parent_span:
    # Do some work in the parent span
    # ...

    # Start a child span
    with start_span("child_operation") as child_span:
        # Do some work in the child span
        # ...

        # Add an event to the child span
        add_event("child_operation_event")

    # Back in the parent span
    add_event("parent_operation_event")
```
