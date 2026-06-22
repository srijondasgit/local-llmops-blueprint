from langchain_openai import OpenAIEmbeddings

# 1. Initialize the embedding connection to LocalAI
embeddings_engine = OpenAIEmbeddings(
    base_url="http://localhost:8080/v1",  # Points to your local Docker setup
    api_key="not-needed",                  # LocalAI ignores this
    model="text-embedding-ada-002"         # Matches your working curl model exactly
)

print("Connecting to LocalAI embedding endpoint via LangChain...")

try:
    # 2. Embed a single string (Equivalent to your curl input)
    text_to_embed = "The quick brown fox jumps over the lazy dog"
    vector = embeddings_engine.embed_query(text_to_embed)

    print("\n✅ Success!")
    print(f"Generated Vector Dimensions: {len(vector)}")
    print(f"Sample of the first 5 vector values: {vector[:5]}")

except Exception as e:
    print(f"\n❌ Connection Error: {e}")
