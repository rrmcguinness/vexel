import time
from trace import start_span, set_attribute, add_event, set_baggage, get_baggage

def example_function():
    # Start a span with a name and some attributes
    with start_span("example_function", 
                   attributes={"function.name": "example_function", "function.type": "example"},
                   baggage_items={"example.context": "test"}) as span:

        # Add an event to the span
        add_event("function_started", {"timestamp": time.time()})

        # Do some work
        time.sleep(0.1)

        # Set an attribute on the span
        set_attribute("work.duration", "100ms")

        # Get baggage item
        context = get_baggage("example.context")
        print(f"Baggage context: {context}")

        # Add another event
        add_event("function_completed", {"timestamp": time.time()})

def nested_spans_example():
    # Start a parent span
    with start_span("parent_operation") as parent_span:
        # Do some work in the parent span
        time.sleep(0.1)

        # Start a child span
        with start_span("child_operation") as child_span:
            # Do some work in the child span
            time.sleep(0.1)

            # Add an event to the child span
            add_event("child_operation_event")

        # Back in the parent span
        add_event("parent_operation_event")

if __name__ == "__main__":
    print("Running tracing example...")

    # Simple span example
    example_function()

    # Nested spans example
    nested_spans_example()

    print("Tracing example completed. Check Google Cloud Trace for results.")
    print("Note: If OpenTelemetry is not installed or Google Cloud Trace is not configured,")
    print("the examples will run with a no-op tracer and no data will be sent to Google Cloud Trace.")
