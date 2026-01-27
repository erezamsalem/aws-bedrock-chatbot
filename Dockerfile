# Use an official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the new AWS-specific LangChain library is installed
RUN pip install --no-cache-dir langchain-aws

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# The command to run when the container starts
CMD ["streamlit", "run", "chatfrontend.py", "--server.port=8501", "--server.address=0.0.0.0"]