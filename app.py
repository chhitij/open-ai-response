import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai_client import OpenAIClient
from utils import upload_pdfs_and_create_vector_store
from dotenv import load_dotenv

# Initialize OpenAI client and vector store
load_dotenv()
client = OpenAIClient().get_client()
auth_token = os.getenv("RENDER_OPEN_AI_AUTH_TOKEN") or "default"
vector_store_details = upload_pdfs_and_create_vector_store()
app = FastAPI()

# Serve a very small frontend from ./static
app.mount("/static", StaticFiles(directory="static"), name="static")


class Query(BaseModel):
    question: str
    auth_token: str


@app.get("/")
def root():
    # Serve the single-page UI
    return FileResponse("static/index.html")


@app.post("/ask")
def ask_openai(query: Query):
    if auth_token == "changeme" or query.auth_token != auth_token:
        return {"error": "Unauthorized"}, 401

    print(f"Vector store id: {vector_store_details['id']}")
    print(f"Received question: {query.question}")
    response = client.responses.create(
        input=query.question,
        model="gpt-5-nano",
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_details['id']],
            "max_num_results": 2
        }],
        # max_output_tokens=1000,
    )

    # Extract annotations / filenames from the response in a defensive way.
    # Different SDK objects (like ResponseFileSearchToolCall) may expose
    # annotations/text directly or inside a .content list. Handle both.
    annotations = []
    file_search_text = None

    for out in getattr(response, "output", []) or []:
        # Case: item has a .content list (each element may have annotations/text)
        if hasattr(out, "content") and out.content:
            for c in out.content:
                if hasattr(c, "annotations") and c.annotations:
                    annotations.extend(list(c.annotations))
                if hasattr(c, "text") and c.text:
                    file_search_text = c.text
        else:
            # Case: the tool call object exposes annotations/text directly
            if hasattr(out, "annotations") and out.annotations:
                annotations.extend(list(out.annotations))
            if hasattr(out, "text") and out.text:
                file_search_text = out.text

    # Get top-k retrieved filenames (annotations may be objects or dict-like)
    retrieved_files = set()
    for a in annotations:
        # object-like
        if hasattr(a, "filename"):
            retrieved_files.add(getattr(a, "filename"))
        # dict-like
        elif isinstance(a, dict) and "filename" in a:
            retrieved_files.add(a["filename"])

    return {
        "answer": response.output_text,
        "files_used": list(retrieved_files),
        "file_search_text": file_search_text
    }
