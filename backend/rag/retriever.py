"""
RAG Retriever for Voice Acting Knowledge

Queries Pinecone vector store to retrieve relevant voice acting techniques
from Stanislavski and Linklater books.
"""
import os
import logging
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

logger = logging.getLogger(__name__)


class VoiceActingRetriever:
    """
    Retriever for voice acting techniques from indexed PDF books.

    Connects to Pinecone vector store and provides semantic search
    over Stanislavski and Linklater texts.
    """

    def __init__(
        self,
        pinecone_api_key: str = None,
        pinecone_index_name: str = None,
        openai_api_key: str = None,
        similarity_top_k: int = 5,
    ):
        """
        Initialize the voice acting retriever.

        Args:
            pinecone_api_key: Pinecone API key (default: from env)
            pinecone_index_name: Pinecone index name (default: from env)
            openai_api_key: OpenAI API key (default: from env)
            similarity_top_k: Number of chunks to retrieve (default: 5)
        """
        # Get configuration from environment if not provided
        pinecone_api_key = pinecone_api_key or os.getenv("PINECONE_API_KEY")
        pinecone_index_name = pinecone_index_name or os.getenv("PINECONE_INDEX_NAME")
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        if not all([pinecone_api_key, pinecone_index_name, openai_api_key]):
            raise ValueError("Missing required API keys or index name in environment")

        logger.info("Initializing VoiceActingRetriever...")

        # Initialize Pinecone
        pc = Pinecone(api_key=pinecone_api_key)
        pinecone_index = pc.Index(pinecone_index_name)

        # Configure embeddings
        embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=openai_api_key,
        )
        Settings.embed_model = embed_model

        # Create vector store and query engine
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        self.vector_index = VectorStoreIndex.from_vector_store(vector_store)
        self.query_engine = self.vector_index.as_query_engine(
            similarity_top_k=similarity_top_k,
            verbose=False,
        )

        self.similarity_top_k = similarity_top_k
        logger.info(f"✅ VoiceActingRetriever initialized (top_k={similarity_top_k})")

    async def search(self, query: str) -> str:
        """
        Search for voice acting techniques.

        Args:
            query: Natural language query about voice acting techniques

        Returns:
            Formatted string with retrieved content and sources
        """
        logger.debug(f"RAG query: {query}")

        # Execute query
        response = self.query_engine.query(query)

        # Format response with sources
        sources = []
        for node in response.source_nodes:
            metadata = node.metadata
            title = metadata.get("title", "Unknown")
            author = metadata.get("author", "Unknown")
            page = metadata.get("page_label", "?")

            sources.append(f"- {title} by {author} (p.{page})")

        # Build formatted result
        result_parts = [str(response.response)]

        if sources:
            result_parts.append("\n\nSources:")
            result_parts.extend(sources)

        result = "\n".join(result_parts)

        logger.debug(f"RAG result: {len(result)} chars, {len(sources)} sources")

        return result

    def search_sync(self, query: str) -> str:
        """
        Synchronous version of search (for non-async contexts).

        Args:
            query: Natural language query about voice acting techniques

        Returns:
            Formatted string with retrieved content and sources
        """
        logger.debug(f"RAG query (sync): {query}")

        # Execute query
        response = self.query_engine.query(query)

        # Format response with sources
        sources = []
        for node in response.source_nodes:
            metadata = node.metadata
            title = metadata.get("title", "Unknown")
            author = metadata.get("author", "Unknown")
            page = metadata.get("page_label", "?")

            sources.append(f"- {title} by {author} (p.{page})")

        # Build formatted result
        result_parts = [str(response.response)]

        if sources:
            result_parts.append("\n\nSources:")
            result_parts.extend(sources)

        result = "\n".join(result_parts)

        logger.debug(f"RAG result: {len(result)} chars, {len(sources)} sources")

        return result


if __name__ == "__main__":
    # For direct testing
    import asyncio
    from dotenv import load_dotenv

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    load_dotenv()

    async def test():
        retriever = VoiceActingRetriever()
        result = await retriever.search("How do I make a character sound more desperate?")
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result)

    asyncio.run(test())
