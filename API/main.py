from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

class User_Question(BaseModel):
    question:str

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def retrieve(question: str):
    return [
        {"text": "test A", "source": "doc A"},
        {"text": "test B", "source": "doc B"},
    ]

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

@app.get("/")
def root():
    return {"message": "test, its working"}

@app.post("/query")
def query(request: User_Question):
    if request.question.strip() == "":
        return {"error": "The query is empty"}
    chunks = retrieve(request.question)
    prompt = prompt_template(request.question, chunks)
    answer = llm_caller(prompt)
    citations = [c["source"] for c in chunks]
    return {
        "answer": answer,
        "citations": citations
    }