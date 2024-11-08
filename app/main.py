from fastapi import FastAPI
from app.routes import vendor_routes
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.staticfiles import StaticFiles
import os
from app.config import settings
from app.tasks.cleanup import scheduler, cleanup_expired_unverified_users  # Import the scheduler to 
from apscheduler.schedulers.base import SchedulerAlreadyRunningError
import pika
from app.rabbitmq.rabbitmq_consumer import consume_vendor_events
from threading import Thread

#from app.database import create_tables


logger = logging.getLogger(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Vendor Service API", 
    version="1.0.0",
    openapi_tags=[
        {"name": "users", "description": "Operations related to managing users"},
        {"name": "reviews", "description": "Operations related to managing reviews"},
        {"name": "orders", "description": "Operations related to managing orders"},
        {"name": "wishlist", "description": "Operations related to managing wishlists"},
    ],
)
# Include the vendor routes
app.include_router(vendor_routes.router, prefix="/vendors", tags=["vendors"])


static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
#@app.on_event("startup")
#async def startup():
    ##create_tables()
    
origins = [
    "http://localhost:3000",  # Your frontend application
]


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
async def startup_event():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        connection.close()
        logger.info("Successfully connected to RabbitMQ")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
    
    # Start the RabbitMQ consumer in a separate thread
    consumer_thread = Thread(target=consume_vendor_events)
    consumer_thread.daemon = True  # This will allow the thread to close when the main process ends
    consumer_thread.start()

    # Ensure the scheduler is running when the app starts
    try:
        if not scheduler.running:
            scheduler.add_job(cleanup_expired_unverified_users, 'interval', hours=24)
            scheduler.start()
            logger.info("Scheduler started for cleaning up unverified users.")
        else:
            logger.info("Scheduler is already running.")
    except SchedulerAlreadyRunningError:
        logger.warning("Attempted to start the scheduler, but it was already running.")
    except Exception as e:
        logger.error(f"Error occurred while starting the scheduler: {e}")
    
    for route in app.router.routes:
        print(route.path, route.name)
       # Ensure the scheduler is running when the app starts
    try:
        # Check if the scheduler is already running before starting
        if not scheduler.running:
            scheduler.add_job(cleanup_expired_unverified_users, 'interval', hours=24)

            scheduler.start()
            logger.info("Scheduler started for cleaning up unverified users.")
        else:
            logger.info("Scheduler is already running.")
    except SchedulerAlreadyRunningError:
        logger.warning("Attempted to start the scheduler, but it was already running.")
    except Exception as e:
        logger.error(f"Error occurred while starting the scheduler: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Service!"}