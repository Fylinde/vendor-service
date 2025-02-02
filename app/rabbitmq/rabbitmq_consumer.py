from app.rabbitmq.rabbitmq_class import RabbitMQConnection  # Assuming the class is saved in rabbitmq_connection.py
import json

def handle_seller_event(ch, method, properties, body):
    """
    Callback function to process messages consumed from the queue.
    """
    try:
        message = json.loads(body)
        print(f"Received message: {message}")

        # Perform logic based on event type
        if message.get("event") == "seller_created":
            seller_data = message["data"]
            # Process seller_data here (e.g., add seller to local database or update seller information)
            print(f"Processing seller data: {seller_data}")

        # Acknowledge message after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Requeue the message if failed

def consume_seller_events():
    # Initialize RabbitMQ connection for consuming
    rabbitmq = RabbitMQConnection(queue_name="seller_queue", exchange_name="seller_events", exchange_type="fanout")

    try:
        rabbitmq.consume_messages(callback=handle_seller_event)
    finally:
        rabbitmq.close_connection()
