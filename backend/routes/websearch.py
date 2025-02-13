from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ragutils.web_search import DuckDuckGoSearchService
from workflow.web_search_indexing import WebSearchIndexingWorkflow

# Initialize router
router = APIRouter(prefix="/websearch", tags=["Web Search"])


# Web Search request model
class WebSearchRequest(BaseModel):
    query: str
    max_results: int = 5  # Default to 3 search results


@router.post("/search/")
async def perform_web_search(request: WebSearchRequest):
    """
    Perform a web search using DuckDuckGo and return indexed results.
    """
    try:
        # Initialize web search service
        search_service = DuckDuckGoSearchService(max_results=request.max_results)
        web_search_workflow = WebSearchIndexingWorkflow(search_service=search_service)

        # Run the workflow asynchronously
        indexed_data = await web_search_workflow.search_and_index(request.query)

        return {"query": request.query, "results": indexed_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
