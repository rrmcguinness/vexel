import time
from logging import get_logger, subscribe, unsubscribe, get_stream_content

def test_logger():
    """Test the logger functionality."""
    # Get a logger instance
    logger = get_logger("test")
    
    # Create a subscriber to demonstrate the stream functionality
    received_logs = []
    
    def log_subscriber(message):
        received_logs.append(message)
        print(f"Subscriber received: {message}")
    
    # Subscribe to the log stream
    subscribe(log_subscriber)
    
    # Log some messages
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Give some time for the logs to be processed
    time.sleep(1)
    
    # Check if the subscriber received the messages
    print(f"Subscriber received {len(received_logs)} messages")
    
    # Get the content of the log stream
    stream_content = get_stream_content()
    print(f"Log stream content length: {len(stream_content)}")
    print("Log stream content preview:")
    print(stream_content[:200] + "..." if len(stream_content) > 200 else stream_content)
    
    # Test buffer size limit by generating a lot of logs
    print("\nTesting buffer size limit...")
    for i in range(1000):
        logger.debug(f"Debug message {i} with some padding to make it longer " + "x" * 100)
    
    # Check the stream content size after generating lots of logs
    stream_content = get_stream_content()
    print(f"Log stream content length after generating lots of logs: {len(stream_content)}")
    print("Buffer should be limited to approximately 1024k bytes")
    
    # Unsubscribe from the log stream
    unsubscribe(log_subscriber)
    
    # Log one more message to verify unsubscription
    logger.info("This message should not be received by the subscriber")
    
    # Check if the subscriber received the last message
    print(f"Subscriber received {len(received_logs)} messages after unsubscribing")
    
    print("\nLogger test completed")

if __name__ == "__main__":
    test_logger()