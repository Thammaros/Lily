import streamlit as st
from config import QDRANT_COLLECTION_NAME, N_RESULTS


@st.cache_data(ttl=300)
def search_top_n_results_by_text(input_text: str):
    """
    Searches the most relevant product informations from Vertiv's product documentation stored in the Qdrant vector database. This includes datasheets, catalogs, and user guides for products such as UPS systems, Rack PDUs, and cooling solutions.
    The function performs a similarity search by embedding the user's query (e.g., product names, features, specifications, or specific technical requirements) and retrieves the top relevant documents from Vertiv’s product database stored in Qdrant.
    Args:
        input_text (str): A query that represents the product or information the user is seeking. 
    Returns:
        str: A combined string of the most relevant product data (e.g., datasheets, specifications, and descriptions) retrieved from the Qdrant database. This output is structured for use in a Retrieval-Augmented Generation (RAG) agent to assist in answering the user query.
    Notes:
        - The function assumes the existence of an embedding model to convert the input query into a vector representation and a Qdrant vector database containing Vertiv product documentation.
        - This function supports Vertiv product documents, including catalogs, datasheets, and installation guides.
        - Queries should be specific to improve search accuracy. 
        - Designed as part of a larger Retrieval-Augmented Generation (RAG) pipeline to enhance AI responses with accurate, document-based data.
    """
    collection_name = QDRANT_COLLECTION_NAME
    n = N_RESULTS

    # Convert the input text into a query vector using the embedding model
    query_vector = list(st.session_state.embedding_model.embed([input_text]))[0]

    # Perform the search in Qdrant
    search_results = st.session_state.qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=n,  # Number of top results to retrieve
    )

    # Process and return the results as a string
    results = []
    for result in search_results:
        point_id = result.id
        score = result.score
        payload = result.payload  # The stored text and other metadata
        results.append({
            "id": point_id,
            "score": score,
            "text": payload.get("text")
        })

    # Combine the text of the results into a single string for context
    context = "\n\n".join(result["text"] for result in results)
    return context


available_functions = {
    'search_top_n_results_by_text':search_top_n_results_by_text,
    }