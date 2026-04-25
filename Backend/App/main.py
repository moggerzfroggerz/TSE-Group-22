from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from schemas import QueryRequest, QueryResponse
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Lifespan")

    app.state.retrieval_service = retrieve

    yield 
    print("Shutting down")


app = FastAPI(lifespan=lifespan)

if settings.Allow_All:
    origins = ["*"]

else:
    origins = [settings.Frontend_Origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def retrieve(question: str):
    return 

def prompt_template(question, chunks):
    context = "\n".join([c["text"] for c in chunks])
    prompt = f"""
    Answer question only using context below 
    Context:
    {context}
    Question
    {question}
    Answer:
    """
    return prompt

def llm_caller(prompt: str):
    return "this is generated answer"

def saftey_application(answer: str):
    return answer

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/retrieve")
def retrieve_endpoint(request: QueryRequest, req: Request):

    retrieval_service = req.app.state.retrieval_service
    
    chunks = retrieval_service(request.question)

    if not chunks:
        raise HTTPException(status_code=404, detail="nothing to retrieve")
    
    return {"chunks": chunks}

@app.post("/answer", response_model=QueryResponse)
def answer(request: QueryRequest, req: Request):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Query is empty")
        
        retrieval_service = req.app.state.retrieval_service
        
        chunks = retrieval_service(request.question)

        if not chunks:
            raise HTTPException(status_code=404, detail="nothing to retrieve")

        prompt = prompt_template(request.question, chunks)

        answer = llm_caller(prompt)
        if not answer:
            raise HTTPException(status_code=500, detail="failed to generate response")

        citations = [c["source"] for c in chunks]

        answer = saftey_application(answer)
        
        return QueryResponse(
            answer=answer,
            citations=citations
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Server error")