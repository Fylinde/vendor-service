from app.rabbitmq.rabbitmq_class import RabbitMQConnection  # Assuming the class is saved in rabbitmq_connection.py
import json

def handle_vendor_event(ch, method, properties, body):
    """
    Callback function to process messages consumed from the queue.
    """
    try:
        message = json.loads(body)
        print(f"Received message: {message}")

        # Perform logic based on event type
        if message.get("event") == "vendor_created":
            vendor_data = message["data"]
            # Process vendor_data here (e.g., add vendor to local database or update vendor information)
            print(f"Processing vendor data: {vendor_data}")

        # Acknowledge message after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Requeue the message if failed

def consume_vendor_events():
    # Initialize RabbitMQ connection for consuming
    rabbitmq = RabbitMQConnection(queue_name="vendor_queue", exchange_name="vendor_events", exchange_type="fanout")

    try:
        rabbitmq.consume_messages(callback=handle_vendor_event)
    finally:
        rabbitmq.close_connection()
