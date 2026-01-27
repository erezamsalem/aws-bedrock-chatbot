import os
# Correct import path for global settings in LangChain v0.3.0+
from langchain_core.globals import set_debug, set_verbose
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# Enable tracing for your terminal logs
set_debug(True)
set_verbose(True)

# --- Database Connection Details ---
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "test1234")
DB_DATABASE = os.getenv("DB_DATABASE", "ai_database")

# Connection string for MySQL
CONNECTION_STRING = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

def get_llm():
    """Initializes the Bedrock LLM using the Amazon Nova Lite regional inference profile."""
    return ChatBedrock(
        region_name=os.getenv("AWS_REGION", "eu-west-1"),
        # 'eu.' prefix is REQUIRED for on-demand regional inference profiles
        model_id="eu.amazon.nova-lite-v1:0", 
        model_kwargs={
            "temperature": 0.5,
            "topP": 0.9,
            "maxTokens": 512, # Nova models use 'maxTokens'
        }
    )

def get_history(session_id):
    """Retrieves chat history from MySQL for the given session."""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=CONNECTION_STRING,
        table_name="message_store"
    )

def get_chat_response(input_text, session_id):
    """Executes the chat chain with history persistence."""
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Provide clear and concise answers."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    response = chain_with_history.invoke(
        {"input": input_text},
        config={"configurable": {"session_id": session_id}}
    )

    return response.content