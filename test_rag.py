from rag.rag_engine import load_knowledge, search_knowledge


# Load scientific knowledge
count = load_knowledge()

print(f"Loaded {count} knowledge files.\n")


# Test question
query = "How does low rainfall affect soil moisture and biodiversity?"

results = search_knowledge(query)


print("RETRIEVED KNOWLEDGE:\n")


for i, document in enumerate(results["documents"][0]):

    source = results["metadatas"][0][i]["source"]
    topic = results["metadatas"][0][i]["topic"]

    print(f"Source: {source}")
    print(f"Topic: {topic}")
    print("-" * 50)

    print(document[:500])

    print("\n" + "=" * 70 + "\n")