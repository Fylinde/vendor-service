from app.rabbitmq.rabbitmq_class import RabbitMQConnection  # Assuming the class is saved in rabbitmq_connection.py


def publish_vendor_created_event(vendor_data: dict):
    # Initialize RabbitMQ connection for publishing
    rabbitmq = RabbitMQConnection(exchange_name="vendor_events", exchange_type="fanout")

    # Publish vendor created event
    try:
        message = {
            "event": "vendor_created",
            "data": vendor_data
        }
        rabbitmq.publish_message(message=message)
    finally:
        rabbitmq.close_connection()
