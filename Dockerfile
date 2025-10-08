# Use an official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
# This includes chatfrontend.py and ChatBackend.py
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# The command to run when the container starts
# This makes the app accessible from outside the container
CMD ["streamlit", "run", "chatfrontend.py", "--server.port=8501", "--server.address=0.0.0.0"]