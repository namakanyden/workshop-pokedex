from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import create_engine, select, Session, or_
from sqladmin import Admin

from models import Pokemon, PokemonAdmin


path = Path(__file__).parent

app = FastAPI(title="Pokédex")
app.mount(
        "/static",
        StaticFiles(directory=path / "static"),
        name="static"
)
templates = Jinja2Templates(directory=path / "templates")

# admin view
engine = create_engine("sqlite:///pokedex.sqlite")
admin = Admin(app, engine)
admin.add_view(PokemonAdmin)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    # render templates
    context = {"request": request, "title": "Vitajte v Pokédexe"}
    return templates.TemplateResponse("home.tpl.html", context)


@app.get("/api/pokemons")
def get_pokemon_list():
    # create statement
    statement = select(Pokemon).limit(50)

    # connect to db and execute query
    session = Session(engine)
    pokemons = session.exec(statement).all()
    session.close()

    # return results
    return pokemons


@app.get("/api/pokemons/{pokedex_number}")
def get_pokemon_detail(pokedex_number: int):
    # create stament
    statement = select(Pokemon).where(Pokemon.pokedex_number == pokedex_number)

    # connect to db and execute query
    session = Session(engine)
    pokemon = session.exec(statement).one_or_none()
    session.close()

    # return results
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found.")
    return pokemon


@app.get('/pokedex', response_class=HTMLResponse)
def view_list_of_pokemons(request: Request, query: str | None = None):
    # create statement
    if query is None:
        statement = select(Pokemon).limit(40)
    else:
        statement = (
            select(Pokemon)
            .where(or_(Pokemon.name.ilike(f'%{query}%'), Pokemon.id == query))
            .limit(40)
        )

    # connect to db and execute query
    session = Session(engine)
    pokemons = session.exec(statement).all()
    session.close()

    # render template
    context = {
        'request': request,
        'title': 'Výsledky hľadania | Pokédex',
        'pokemons': pokemons
    }

    return templates.TemplateResponse('pokemon-list.tpl.html', context)


@app.get("/pokedex/{pokedex_number}", response_class=HTMLResponse)
def view_detail_of_pokemon(request: Request, pokedex_number: int):
    # create statement
    statement = select(Pokemon).where(Pokemon.pokedex_number == pokedex_number)

    # connect to db and execute query
    session = Session(engine)
    pokemon = session.exec(statement).one_or_none()
    session.close()

    # process results and render templates
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
