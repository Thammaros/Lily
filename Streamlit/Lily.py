import streamlit as st
from ollama_utils import run_model
from utils import (init, 
                   render_chat_history)
from config import CHAT_HISTORY_LENGTH


def main():
    init()
    # Chat input
    if user_input := st.chat_input("Type your message..."):
        # st.write(st.session_state.chat_history[1:]) #For DEBUG
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        #Limiting Chat history length
        if len(st.session_state.chat_history)>CHAT_HISTORY_LENGTH:
            st.session_state.chat_history = [{'role': 'system', 'content': st.session_state.SYSTEM_PROMPT}]+st.session_state.chat_history[-(CHAT_HISTORY_LENGTH-1):]
        # Generate Agent's response
        with st.spinner("Generating response..."):
           run_model()
    # Display the chat history 
    render_chat_history()


if __name__ == "__main__":
    main()