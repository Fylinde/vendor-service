FROM python:3.9

WORKDIR /app

ENV PYTHONPATH=/app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip 

# Add this line to install nano
RUN apt-get update && apt-get install -y nano

# Add this line to install ping
RUN apt-get update && apt-get install -y iputils-ping

# Add this line to install curl
RUN apt-get install -y curl

# Add this line to install alembic
RUN pip install alembic

# Add this line to install psql
RUN apt-get install -y postgresql-client


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install bcrypt
RUN pip install bcrypt

# Copy the app directory and other necessary files
COPY app /app/app
#COPY tests /app/tests
COPY alembic.ini /app/alembic.ini
COPY start.sh /app/start.sh
COPY wait-for-it.sh /app/wait-for-it.sh

# Make the start.sh script executable
RUN chmod +x /app/start.sh

# Expose the port
EXPOSE 8012

# Command to run the application
CMD ["/app/start.sh"]