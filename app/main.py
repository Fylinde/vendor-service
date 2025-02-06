from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import pika
from app.config import settings
from contextlib import asynccontextmanager
from threading import Thread
from app.tasks.cleanup import scheduler, cleanup_expired_unverified_users
from app.routes import seller_routes, ratings, seller_transactions, live_shopping_session
from app.rabbitmq.rabbitmq_consumer import consume_seller_events
from celery import Celery



# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        connection.close()
        logger.info("Successfully connected to RabbitMQ")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")

    consumer_thread = Thread(target=consume_seller_events)
    consumer_thread.daemon = True
    consumer_thread.start()

    try:
        if not scheduler.running:
            scheduler.add_job(cleanup_expired_unverified_users, "interval", hours=24)
            scheduler.start()
            logger.info("Scheduler started for cleaning up unverified users.")
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")

    await log_routes(app)
    yield

    logger.info("Shutting down application...")
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped.")

async def log_routes(app: FastAPI):
    """Logs all registered routes safely (handles WebSocket routes)"""
    logger.info("Available Routes:")
    for route in app.routes:
        if hasattr(route, "methods"):  # ✅ Only log methods for HTTP routes
            logger.info(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
        else:  # ✅ Handle WebSocket routes separately
            logger.info(f"Path: {route.path}, Name: {route.name}, WebSocket Route")


app = FastAPI(
    title="Seller Service API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # React frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(seller_routes.router, prefix="/sellers", tags=["sellers"])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(seller_transactions.router, prefix="/payments/escrow", tags=["payments"])
app.include_router(live_shopping_session.router, prefix="/live-shopping", tags=["live-shopping"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Seller Service!"}

celery = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.timezone = 'UTC'
celery.conf.task_routes = {
    'tasks.cleanup.run_check_inactive_sellers': {'queue': 'cleanup'},
}

@app.post("/register_seller")
async def register_seller(data: dict):
    return {"message": "Seller registered successfully"}


@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is configured correctly!"}
