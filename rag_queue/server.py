from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(
        query:str = Query(..., description="The user's query")
        ):
    job = queue.enqueue(process_query, query)

    return {"status": "queued", "job_id": job.id}

@app.get("/job-status")
def get_result(job_id: str = Query(..., description="The ID of the job to check")):

    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    
    return {"status": job.get_status(), "result": result}