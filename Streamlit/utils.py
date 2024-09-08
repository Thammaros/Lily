import streamlit as st
import inspect
from cache_utils import (load_prompts, 
                         init_ollama_client, 
                         init_qdrant_client, 
                         init_embed_model)
from config import (INIT_STYLE, 
                    AGENT_NAME, 
                    PAGE_TITLE, 
                    PAGE_ICON)


def init():
    st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout="wide",
            initial_sidebar_state="expanded"
            )
    st.markdown(INIT_STYLE, unsafe_allow_html=True)
    st.title(AGENT_NAME)
    SYSTEM_PROMPT, STARTING_PROMPT = load_prompts()
    if 'SYSTEM_PROMPT' not in st.session_state:
        st.session_state.SYSTEM_PROMPT = SYSTEM_PROMPT
    if 'STARTING_PROMPT' not in st.session_state:
        st.session_state.STARTING_PROMPT = STARTING_PROMPT
    if 'qdrant_client' not in st.session_state:
        st.session_state.qdrant_client = init_qdrant_client()
    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = init_embed_model()
    if 'ollama_client' not in st.session_state:
        st.session_state.ollama_client = init_ollama_client()
    # Initialize session state for chat history if not already set
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{'role': 'system', 'content': st.session_state.SYSTEM_PROMPT},
                                         {'role': 'assistant', 'content': st.session_state.STARTING_PROMPT}
                                         ]
        

def render_chat_history():
    # Display the chat history 
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['role'] not in {'tool', 'system'}:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])


def generate_function_description(func):
    func_name = func.__name__
    docstring = func.__doc__ or f'Function {func_name}'

    # Get the function's parameters
    sig = inspect.signature(func)
    params = sig.parameters

    properties = {}
    required = []

    # Extract parameter descriptions from the docstring
    arg_descriptions = {}
    if docstring:
        lines = docstring.strip().split('\n')
        current_arg = None
        for line in lines:
            line = line.strip()
            if ':' in line:
                parts = line.split(':', 1)
                if parts[0] in params:
                    current_arg = parts[0]
                    arg_descriptions[current_arg] = parts[1].strip()
            elif current_arg:
                arg_descriptions[current_arg] += ' ' + line.strip()

    # Build the properties and required lists
    for param_name, param in params.items():
        param_type = 'string'  # Default type
        if param.annotation != inspect.Parameter.empty:
            param_type = param.annotation.__name__.lower()

        param_description = arg_descriptions.get(param_name, f'The name of the {param_name}')

        properties[param_name] = {
            'type': param_type,
            'description': param_description,
        }
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    # Assemble the final function description
    function_description = {
        'type': 'function',
        'function': {
            'name': func_name,
            'description': docstring,
            'parameters': {
                'type': 'object',
                'properties': properties,
                'required': required,
            },
        },
    }

    return function_description