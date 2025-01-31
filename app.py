import streamlit as st
from openai import OpenAI
from openai import APIError
import time

# Initialize OpenAI client
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Failed to initialize OpenAI client. Please check your API key.")
    st.stop()

# Set page configuration
st.set_page_config(page_title="Kunal's ChatGPT Clone", page_icon="💭")

# Initialize session state for message history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Display chat title
st.title("💭 Kunal's ChatGPT Clone")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Display assistant response with a typing indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Send request to OpenAI API
            for response in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} 
                         for m in st.session_state.messages],
                stream=True,
            ):
                # Extract response content
                full_response += (response.choices[0].delta.content or "")
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            
            # Display final response
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
            
        except APIError as e:
            st.error(f"OpenAI API Error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add a sidebar with some information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This is a simple ChatGPT clone built with:
    - Streamlit
    - OpenAI API
    - Python
    
    The app maintains conversation history and streams responses in real-time.
    """) 