from app.rabbitmq.rabbitmq_class import RabbitMQConnection  # Assuming the class is saved in rabbitmq_connection.py


def publish_seller_created_event(seller_data: dict):
    # Initialize RabbitMQ connection for publishing
    rabbitmq = RabbitMQConnection(exchange_name="seller_events", exchange_type="fanout")

    # Publish seller created event
    try:
        message = {
            "event": "seller_created",
            "data": seller_data
        }
        rabbitmq.publish_message(message=message)
    finally:
        rabbitmq.close_connection()
