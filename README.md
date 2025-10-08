Persistent AI Chatbot with AWS Bedrock, MySQL, and Docker
Overview
This project is a fully-featured, conversational AI chatbot built with a powerful tech stack. It uses AWS Bedrock (with the Amazon Titan model) as its reasoning engine, a Streamlit frontend for a clean user interface, and a MySQL database for permanent conversation history. The entire application is containerized using Docker and Docker Compose for easy setup and deployment.

This version moves beyond a simple in-memory prototype to a persistent application where conversations are saved and can be continued across sessions.

Features
Conversational AI: Powered by the Amazon Titan Text Express v1 model via AWS Bedrock.

Permanent History: Chat conversations are stored and retrieved from a MySQL database, ensuring no data is lost.

Interactive UI: A clean, responsive, and real-time chat interface built with Streamlit.

Dark Mode Default: The app is configured to launch in a user-friendly dark mode.

Containerized: Fully configured with a Dockerfile and docker-compose.yml for one-command setup.

Secure Configuration: Uses a .env file to securely manage all credentials (AWS and Database).

Architecture
The application is composed of three main layers that work together:

Streamlit Frontend (chatfrontend.py): The user-facing web interface. It captures user input and displays the conversation history. It manages a session_id to identify which conversation to load.

LangChain Backend (ChatBackend.py): The application's "brain." It receives requests from the frontend, uses SQLChatMessageHistory to fetch the relevant conversation from the MySQL database, constructs a prompt, and sends it to AWS Bedrock.

MySQL Database: The persistence layer. The message_store table holds the entire history of all conversations, linked by session_id.

[User] -> [Streamlit UI] -> [LangChain Backend] -> [MySQL DB (for history)] -> [AWS Bedrock (for AI response)] -> [Backend] -> [UI]

Prerequisites
Before you begin, ensure you have the following installed and configured:

Python 3.11

Docker Desktop

A running MySQL Server instance (local or remote)

An AWS Account with Amazon Bedrock access enabled for the Titan model

AWS CLI configured with your credentials (aws configure)

Project Setup
There are two ways to set up and run this project: using Docker (recommended) or running it locally.

1. Docker Setup (Recommended)
This is the easiest way to get started.

Clone the repository:

git clone <repository-url>
cd <repository-name>

Configure Environment Variables:

Create a copy of the example environment file: cp .env.example .env

Open the new .env file and fill in your actual AWS credentials and your MySQL password.

Create the Database:

Connect to your MySQL server.

Create the database and the required table by running the following SQL commands:

CREATE DATABASE ai_database;
USE ai_database;
CREATE TABLE message_store (id INT AUTO_INCREMENT PRIMARY KEY, session_id VARCHAR(255) NOT NULL, message TEXT NOT NULL, INDEX idx_session_id (session_id));

Build and Run with Docker Compose:

docker-compose up --build

This command will build the Docker image and start the application. Open your browser to http://localhost:8501.

2. Local Setup (Without Docker)
Clone and set up the environment as described in steps 1-3 of the Docker setup.

Create a Python Virtual Environment:

python -m venv .venv
.\.venv\Scripts\Activate

Install Dependencies:

The project now includes a requirements.txt file. Install all packages with:

pip install -r requirements.txt

Usage
To start the app (Docker):

docker-compose up

To start the app (Local):

streamlit run chatfrontend.py

To stop the app (Docker):

docker-compose down

File Structure
The project directory is organized as follows:

.
├── .streamlit/
│   └── config.toml        # Configures Streamlit theme (e.g., dark mode)
├── .env                   # Your secret credentials (ignored by git)
├── .env.example           # Template for environment variables
├── .gitignore             # Tells git which files to ignore
├── ChatBackend.py         # Backend logic, DB connection, and Bedrock integration
├── chatfrontend.py        # Streamlit frontend UI code
├── docker-compose.yml     # Defines the Docker services
├── Dockerfile             # Instructions to build the application's Docker image
├── requirements.txt       # List of all Python dependencies
└── README.md              # Project documentation
