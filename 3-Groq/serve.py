import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
load_dotenv()

grok_api_key = os.getenv("GROK_API_KEY")
model = ChatGroq(model="gemma2-9b-it", api_key=grok_api_key)

# 1.Create prompt template
system_template = "Translate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text1}")
    ]
)

parser = StrOutputParser()

# Create chain
chain = prompt_template|model|parser

# App definition
app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API server using langchain runnable interfaces")

# Adding chain routes
add_routes(
    app=app,
    runnable=chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

# Use python serve.py to execute