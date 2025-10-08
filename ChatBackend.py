# Import functions
import os
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import BedrockChat
from langchain.chains import ConversationChain
from langchain_community.chat_message_histories import SQLChatMessageHistory

# --- Database Connection Details ---
# Read database configuration from environment variables for Docker
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "test1234")
DB_DATABASE = os.getenv("DB_DATABASE", "ai_database")

# This is the connection string LangChain will use
CONNECTION_STRING = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
# --- End of Database Connection Details ---


# function to invoke model
def get_llm():
    llm = BedrockChat(
        region_name=os.getenv("AWS_REGION", "eu-west-1"), # Read AWS region from environment
        model_id="amazon.titan-text-express-v1", #set the foundation model
        model_kwargs= {                      #configure the properties for Titan
            "temperature": 1,
            "topP": 0.5,
            "maxTokenCount": 400, # Increased token count for better responses
        }
    )
    return llm

# New function to get chat history from the database for a specific session
def get_history(session_id):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=CONNECTION_STRING, # <-- Updated to 'connection' to fix warning
        table_name="message_store"
    )

##Create a chat client function
def get_chat_response(input_text, session_id):

    llm = get_llm()

    # Get the history from the database
    message_history = get_history(session_id)

    # Create a memory object that uses our database-backed history
    memory = ConversationBufferMemory(
        memory_key="history",
        chat_memory=message_history,
        return_messages=True
    )

    conversation_with_memory = ConversationChain(
        llm = llm,
        memory = memory,
        verbose = True
    )

    # When we invoke the chain, it will automatically:
    # 1. Load the history from the database.
    # 2. Add the new user message.
    # 3. Call the AI model.
    # 4. Save the new user message and the AI response back to the database.
    chat_response = conversation_with_memory.invoke(input = input_text)

    return chat_response['response']