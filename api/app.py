from fastapi import FastAPI

app = FastAPI()


@app.get('/ollama')
def read_ollama():
    return {'Hello': 'Ollama'}


@app.get('/openai')
def read_openai():
    return {'Hello': 'OpenAI'}


@app.get('/cohere')
def read_cohere():
    return {'Hello': 'Cohere'}


@app.get('/palm')
def read_palm():
    return {'Hello': 'Palm'}
