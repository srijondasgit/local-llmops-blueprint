from langchain_core.globals import set_llm_cache
from langchain_community.cache import RedisSemanticCache
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Initialize a local embedding model to turn text into mathematical meaning
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Tell Redis to use Semantic Caching with a 5% error tolerance (distance threshold)
set_llm_cache(
    RedisSemanticCache(
        redis_url="redis://localhost:6379", 
        embedding=embeddings,
        score_threshold=0.05
    )
)
