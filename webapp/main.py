import os
import openai
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Body(BaseModel):
    query: str


@app.get("/")
def root():
    return RedirectResponse(url="/docs", status_code=301)


@app.post("/ask")
def ask(body: Body):
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Assistant is a chatbot that helps you."},
                {"role": "user", "content": body.query},
            ],
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
