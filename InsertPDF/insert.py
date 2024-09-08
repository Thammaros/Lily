import argparse
from fastembed import TextEmbedding
from qdrant_client import AsyncQdrantClient, models
from tqdm import tqdm
import asyncio, PyPDF2, uuid, re, os, gc

def preprocess_text(text:str):
    text = re.sub(r'\s+', ' ', text.strip().lower())
    return text

async def process_and_embed_pdfs_in_directory(pdf_directory, collection_name, embedding_model, qdrant_client):
    """
    Processes PDF files in a given directory, converts each page's text into vector embeddings,
    and stores them in a Qdrant vector database.

    Args:
        pdf_directory (str): Path to the directory containing PDF files.
        collection_name (str): Name of the Qdrant collection where the embeddings will be stored.

    Returns:
        None
    """
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            pdf_size = os.path.getsize(pdf_path)

            print(f"Processing file: {pdf_file} | Size: {pdf_size / (1024 * 1024):.2f} MB")

            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    number_of_pages = len(reader.pages)

                    for page_num in tqdm(range(number_of_pages), desc=f"Processing {pdf_file} pages", leave=False):
                        page = reader.pages[page_num]
                        text = page.extract_text()

                        text = preprocess_text(text)
                        formatted_text = f"From {pdf_file.split('.')[0]}, Page no {page_num + 1}\n{text}"
                        embedding = list(embedding_model.embed([formatted_text]))[0]

                        point = models.PointStruct(
                            id=str(uuid.uuid5(uuid.NAMESPACE_URL, formatted_text)),
                            vector=embedding,
                            payload={"text": formatted_text}
                        )

                        await qdrant_client.upsert(collection_name=collection_name, points=[point], wait=False)

            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
            finally:
                gc.collect()

async def main(QDRANT_HOST, EMBED_MODEL, QDRANT_COLLECTION_NAME, VECTOR_SIZE, PDF_DIRECTORY):
    qdrant_client = AsyncQdrantClient(host=QDRANT_HOST, grpc_port=6334, prefer_grpc=True)
    embedding_model = TextEmbedding(model_name=EMBED_MODEL)

    if not await qdrant_client.collection_exists(collection_name=QDRANT_COLLECTION_NAME):
        await qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )

    await process_and_embed_pdfs_in_directory(PDF_DIRECTORY, QDRANT_COLLECTION_NAME, embedding_model, qdrant_client)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and embed PDFs into Qdrant using text embeddings.")
    
    parser.add_argument('--qdrant_host', type=str, default="10.8.0.1", help="Qdrant host IP")
    parser.add_argument('--embed_model', type=str, default='nomic-ai/nomic-embed-text-v1.5-Q', help="Text embedding model")
    parser.add_argument('--qdrant_collection_name', type=str, default="Vertiv", help="Qdrant collection name")
    parser.add_argument('--vector_size', type=int, default=768, help="Vector size for embeddings")
    parser.add_argument('--pdf_directory', type=str, default="./PDF", help="Directory containing PDFs to process")

    args = parser.parse_args()

    asyncio.run(main(
        QDRANT_HOST=args.qdrant_host,
        EMBED_MODEL=args.embed_model,
        QDRANT_COLLECTION_NAME=args.qdrant_collection_name,
        VECTOR_SIZE=args.vector_size,
        PDF_DIRECTORY=args.pdf_directory
    ))

# python3 insert.py --qdrant_host "127.0.0.1" --embed_model "nomic-ai/nomic-embed-text-v1.5-Q" --qdrant_collection_name "Vertiv" --vector_size 768 --pdf_directory "./PDF"
