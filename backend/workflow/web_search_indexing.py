import logging
from typing import Dict, List

from services.ragutils import CustomSegment, EmbeddingService, Indexer, WebSearchService

logger = logging.getLogger(__name__)


class WebSearchIndexingWorkflow:
    """
    Example workflow that:
      1. Does a web search (via a chosen web search service).
      2. Chunks + Embeds the search results.
      3. Returns or persists them (the example returns them as a list).
    """

    def __init__(
        self,
        search_service: WebSearchService,
        segmenter: CustomSegment = None,
        embedder: EmbeddingService = None,
    ):
        """
        :param search_service: An instance of a web search service,
                               e.g. DuckDuckGoSearchService or LangChainWebSearchService
        :param segmenter: Your custom segmentation logic
        :param embedder: Your embedding service
        """
        self.search_service = search_service
        self.segmenter = segmenter if segmenter else CustomSegment()
        self.embedder = embedder if embedder else EmbeddingService()
        self.indexer = Indexer(segmenter=self.segmenter, embedder=self.embedder)

    async def search_and_index(self, query: str) -> List[Dict]:
        """
        1) search_and_scrape for `query`
        2) chunk each result
        3) embed & store them
        4) return the final indexed data
        """
        logger.info(f"Starting web search for query: {query}")

        # 1) Perform the search
        raw_results = self.search_service.search_and_scrape(query)
        logger.info(f"Got {len(raw_results)} results for query: {query}")

        # 2) Prepare a list of "documents" to feed to the indexer
        documents_to_process = []
        for i, result in enumerate(raw_results):
            doc_id = f"web-{i}"
            text_content = result.get("raw_text", "")
            meta = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("body_snippet", ""),
            }
            documents_to_process.append(
                {"document_id": doc_id, "text": text_content, "metadata": meta}
            )

        # 3) Index them (async)
        indexed_data_list = await self.indexer.index_documents(documents_to_process)
        logger.info(
            f"Completed indexing {len(indexed_data_list)} documents from web search."
        )
        return indexed_data_list
