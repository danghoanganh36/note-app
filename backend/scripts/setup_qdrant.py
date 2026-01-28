import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

# Initialize Qdrant client with cluster endpoint
client = QdrantClient(
    url=os.getenv("QDRANT_CLUSTER_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

collection_name = "handbook-vectors"

# Check if collection exists
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if collection_name not in collection_names:
    # Create collection with sentence-transformers/all-MiniLM-L6-v2 dimension
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,  # sentence-transformers/all-MiniLM-L6-v2
            distance=Distance.COSINE
        )
    )
    print(f"✅ Collection '{collection_name}' created successfully")
else:
    print(f"ℹ️  Collection '{collection_name}' already exists")

# Get collection info
collection_info = client.get_collection(collection_name)
print(f"📊 Collection stats:")
print(f"   - Vectors count: {collection_info.points_count}")
print(f"   - Vector size: {collection_info.config.params.vectors.size}")
print(f"   - Distance: {collection_info.config.params.vectors.distance}")
print(f"   - Status: {collection_info.status}")
