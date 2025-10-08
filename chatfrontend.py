import streamlit as st
import ChatBackend as glib
import uuid # We'll keep this import for later

# Set the page title and header
st.set_page_config(page_title="Chatbot")
st.title("Persistent Chatbot")

# --- Session ID Management ---
# For testing, we will use a FIXED session ID to ensure the same
# conversation is loaded every time you refresh the page.
if 'session_id' not in st.session_state:
    st.session_state.session_id = "my_test_session" # <-- FIXED ID FOR TESTING
# --- End of Session ID Management ---


# --- Display Chat History from Database ---
# Get the message history object from the backend for the current session.
# This object reads directly from your 'message_store' table.
try:
    message_history = glib.get_history(st.session_state.session_id)

    # Re-render the chat history from the database on every page interaction
    for message in message_history.messages:
        # Use the message type ("human" or "ai") to display the correct chat bubble
        with st.chat_message(message.type):
            st.markdown(message.content)
except Exception as e:
    st.error(f"Could not load chat history. Please ensure the database is running and configured correctly. Error: {e}")
# --- End of Display Chat History ---


# Display the chat input box at the bottom of the screen
input_text = st.chat_input("Chat with your bot here")

# This block runs only when the user types something and presses Enter
if input_text:
    # Display the user's new message immediately
    with st.chat_message("user"):
        st.markdown(input_text)

    # Call the backend, passing the user's message and the unique session_id.
    # The backend will handle saving this new message and the AI's response to the DB.
    try:
        chat_response = glib.get_chat_response(
            input_text=input_text,
            session_id=st.session_state.session_id
        )
        # Display the AI's response
        with st.chat_message("assistant"):
            st.markdown(chat_response)
    except Exception as e:
        st.error(f"Failed to get a response from the chatbot. Error: {e}")