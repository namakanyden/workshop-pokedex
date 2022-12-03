import uvicorn
from fastapi import FastAPI


app = FastAPI(title="Pokédex")


@app.get("/")
def hello():
    return "Hello world!"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8080,       # port, na ktorom sa aplikácia spustí, default=8000
        host="0.0.0.0",  # bude akceptovať komunikáciu z akejkoľvek IP adresy, default=127.0.0.1
        reload=True,     # v prípade zmeny súboru sa aplikácia automaticky reštartne, default=False
    )
