import os
import sys
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from chain import get_chain, calculate_embeddings_rag
app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/compute_embeddings")
async def store_embeddings():
    return calculate_embeddings_rag()

# Edit this to add the chain you want to add
chain = get_chain()
add_routes(app, chain, enable_feedback_endpoint=True)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
