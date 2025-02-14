import streamlit as st
from ollama_instance import get_response
from session_state import initialise_session_state, disable_chat_input


# Initialise session state and run the app
st.title("Ollama Chatbot powered by Streamlit😀")

initialise_session_state()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Say something", disabled=st.session_state.processing, on_submit=disable_chat_input):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.spinner("AI is thinking..."):
        full_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        ai_response = get_response(full_prompt)

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
        
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Re-enable chat input
    st.session_state.processing = False
    
    # Rerun the app to update the chat history
    st.rerun()