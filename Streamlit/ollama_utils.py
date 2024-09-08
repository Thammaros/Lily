import streamlit as st
from tools import available_functions
from utils import generate_function_description
from config import (OLLAMA_MODEL,
                    OLLAMA_OPTIONS)


def run_model():
    # loop until final response 
    while True:
        response = st.session_state.ollama_client.chat(
            model=OLLAMA_MODEL,
            messages=st.session_state.chat_history,
            tools=[generate_function_description(func) for func in available_functions.values()],
            options=OLLAMA_OPTIONS)
        # Check if any tool calls
        if response['message'].get('tool_calls'):
            for tool_call in response['message']['tool_calls']:
                function_name = tool_call['function']['name']
                arguments = tool_call['function']['arguments']
                if function_name in available_functions:
                    try:
                        function_response = available_functions[function_name](**arguments)
                        st.session_state.chat_history.append({'role': 'tool', 'content': f'Calling tool: {function_name} with arguments {arguments}\n\nResults: ' + str(function_response)})
                    except Exception as e:
                        st.session_state.chat_history.append({'role': 'tool', 'content': f'Calling tool: {function_name} with arguments {arguments}\nResults: ' + str({"error": str(e)})})
                else:
                    st.session_state.chat_history.append({'role': 'tool', 'content': f"Function '{function_name}' not recognized."})
        # no tool calls just text response then break
        else:
            st.session_state.chat_history.append({'role': 'assistant', 'content': response['message']['content']})
            break
