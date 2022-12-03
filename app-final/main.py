import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import create_engine, select, Session, or_
from sqladmin import Admin

from models import Pokemon, PokemonAdmin


app = FastAPI(title="Pokédex")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# admin view
engine = create_engine("sqlite:///pokedex.sqlite")
admin = Admin(app, engine)
admin.add_view(PokemonAdmin)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {"request": request, "title": "Vitajte v Pokédexe"}
    return templates.TemplateResponse("home.tpl.html", context)


@app.get("/api/pokemons")
def get_pokemon_list():
    with Session(engine) as session:
        statement = select(Pokemon).limit(50)
        pokemons = session.exec(statement).all()
        return pokemons


@app.get("/api/pokemons/{pokedex_number}")
def get_pokemon_detail(pokedex_number: int):
    with Session(engine) as session:
        statement = select(Pokemon).where(Pokemon.pokedex_number == pokedex_number)
        pokemon = session.exec(statement).one_or_none()
        if pokemon is None:
            raise HTTPException(status_code=404, detail="Pokemon not found.")
        return pokemon


@app.get('/pokedex', response_class=HTMLResponse)
def view_list_of_pokemons(request: Request, q: str | None = None):
    with Session(engine) as session:
        if q is None:
            statement = select(Pokemon).limit(40)
        else:
            statement = (
                select(Pokemon)
                .where(or_(Pokemon.name.ilike(f'%{q}%'), Pokemon.id == q))
                .limit(40)
            )
        pokemons = session.exec(statement).all()

        context = {
            'request': request,
            'title': 'Výsledky hľadania | Pokédex',
            'pokemons': pokemons
        }

        return templates.TemplateResponse('pokemon-list.tpl.html', context)


@app.get("/pokedex/{pokedex_number}", response_class=HTMLResponse)
def view_detail_of_pokemon(request: Request, pokedex_number: int):
    with Session(engine) as session:
        statement = select(Pokemon).where(Pokemon.pokedex_number == pokedex_number)
        pokemon = session.exec(statement).one_or_none()
        if pokemon is None:
            context = {
                "request": request,
                "title": "Pokémon sa nenašiel | Pokédex"
            }
            return templates.TemplateResponse("404.tpl.html", context)

        context = {
            "request": request,
            "title": f"{pokemon.name} | Pokédex",
            "pokemon": pokemon,
        }

        return templates.TemplateResponse("pokemon-detail.tpl.html", context)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8080,  # port, na ktorom sa aplikácia spustí, default=8000
        host="0.0.0.0",  # bude akceptovať komunikáciu z akejkoľvek IP adresy, default=127.0.0.1
        reload=True,  # v prípade zmeny súboru sa aplikácia automaticky reštartne, default=False
    )
