SYSTEM_PROMPT_PATH = './system_prompt.txt'
STARTING_PROMPT_PATH = './starting_prompt.txt'

EMBED_MODEL = 'nomic-ai/nomic-embed-text-v1.5-Q'

# OLLAMA_HOST = "http://host.docker.internal:11434"
OLLAMA_HOST = "http://ollama:11434"
OLLAMA_MODEL = 'llama3.1'
OLLAMA_OPTIONS = {
    # "seed": 100,                 
    # "temperature": 0.05, 
    "num_ctx": 8192,                  
    "num_predict": -1,          
}

QDRANT_HOST = "qdrant"
QDRANT_COLLECTION_NAME = "Vertiv"

N_RESULTS = 5  
CHAT_HISTORY_LENGTH = 10

PAGE_TITLE = "Lily"
PAGE_ICON = "😎"
AGENT_NAME = "Lily🤓"
INIT_STYLE = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    [data-testid="stSidebarNav"] {
        position: absolute;
        width: 100%;
        margin-top: 220px;
    }

    [data-testid="stSidebarNav"] ul {
        padding-top: 10px;
    }
    </style>
"""

