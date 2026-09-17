import chromadb

from pathlib import Path

from chromadb.utils import embedding_functions


# ==========================================================
# EMBEDDING MODEL
# ==========================================================

embedding_model = (
    embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)


# ==========================================================
# CHROMA DATABASE
# ==========================================================

client = chromadb.PersistentClient(
    path="data/chroma_db"
)


collection = client.get_or_create_collection(
    name="biodiversity_knowledge",
    embedding_function=embedding_model
)


# ==========================================================
# LOAD KNOWLEDGE
# ==========================================================

def load_knowledge():

    knowledge_folder = Path("knowledge")

    documents = []
    ids = []
    metadatas = []


    for file in knowledge_folder.glob("*.md"):

        text = file.read_text(
            encoding="utf-8"
        )

        if not text.strip():
            continue


        documents.append(text)

        ids.append(
            file.stem
        )

        metadatas.append(
            {
                "source": file.name,
                "topic": file.stem
            }
        )


    if documents:

        collection.upsert(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )


    return len(documents)


# ==========================================================
# SEARCH KNOWLEDGE
# ==========================================================

def search_knowledge(
    query,
    n_results=4
):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results