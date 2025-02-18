import json
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from routes.utils import clean_result
from services.ragutils.web_search import DuckDuckGoSearchService
from workflow.web_search_indexing import WebSearchIndexingWorkflow

router = APIRouter(prefix="/websearch", tags=["Web Search"])


class WebSearchRequest(BaseModel):
    """
    Defines the request payload for web search.
    """

    query: str
    max_results: int = 5  # Default to 5 results


@router.post("/search/")
async def perform_web_search(request: WebSearchRequest):
    """
    Perform a web search using DuckDuckGo and return indexed results.

    Args:
        request (WebSearchRequest): JSON payload containing `query` and optional `max_results`.

    Returns:
        dict: JSON response with search results.
    """
    try:
        start_time = time.time()

        # Initialize web search
        search_service = DuckDuckGoSearchService(max_results=request.max_results)
        web_search_workflow = WebSearchIndexingWorkflow(search_service=search_service)

        # Run workflow
        indexed_data = await web_search_workflow.search_and_index(request.query)

        # Clean search results
        cleaned_data = [clean_result(doc) for doc in indexed_data]
        json_safe_data = json.loads(
            json.dumps(cleaned_data, default=str, ensure_ascii=False)
        )

        return {
            "query": request.query,
            "results": json_safe_data,
            "elapsed_time": round(time.time() - start_time, 2),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
