import concurrent
import os

from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from openai_client import OpenAIClient

client = OpenAIClient().get_client()

def upload_single_pdf(file_path: str, vector_store_id: str):
  file_name = os.path.basename(file_path)
  try:
      file_response = client.files.create(file=open(file_path, 'rb'), purpose="assistants")
      attach_response = client.vector_stores.files.create(
          vector_store_id=vector_store_id,
          file_id=file_response.id
      )
      return {"file": file_name, "status": "success"}
  except Exception as e:
      print(f"Error with {file_name}: {str(e)}")
      return {"file": file_name, "status": "failed", "error": str(e)}

def upload_pdf_files_to_vector_store(vector_store_id: str):
    pdf_files = [os.path.join('docs', f) for f in os.listdir('docs') if f.endswith('.pdf')]
    stats = {"total_files": len(pdf_files), "successful_uploads": 0, "failed_uploads": 0, "errors": []}
    
    print(f"{len(pdf_files)} PDF files to process. Uploading in parallel...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(upload_single_pdf, file_path, vector_store_id): file_path for file_path in pdf_files}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(pdf_files)):
            result = future.result()
            if result["status"] == "success":
                stats["successful_uploads"] += 1
            else:
                stats["failed_uploads"] += 1
                stats["errors"].append(result)

    return stats

def create_vector_store(store_name: str) -> dict:
    try:
      vector_stores = client.vector_stores.list()
      for vs in vector_stores.data:
        if vs.name == store_name:
          return {
            "id": vs.id,
            "name": vs.name,
            "created_at": vs.created_at,
            "file_count": vs.file_counts.completed,
            "created": False
          }
          
      vector_store = client.vector_stores.create(name=store_name)
      details = {
          "id": vector_store.id,
          "name": vector_store.name,
          "created_at": vector_store.created_at,
          "file_count": vector_store.file_counts.completed,
          "created": True
      }
      print("Vector store created:", details)
      
      return details
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return {}

def upload_pdfs_and_create_vector_store():
  store_name = "open_ai_responses_rag_vector_store"
  vector_store_details = create_vector_store(store_name)
  print(f"Vector Store Details: {vector_store_details}")

  if vector_store_details["created"]:
    stats = upload_pdf_files_to_vector_store(vector_store_details['id'])
    print("Upload Stats:", stats)
  
  return vector_store_details
