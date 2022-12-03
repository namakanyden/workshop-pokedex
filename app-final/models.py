from sqladmin import ModelView
from sqlmodel import Field, SQLModel


class Pokemon(SQLModel, table=True):
    # __tablename__ = "pokemon"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    pokedex_number: int
    classification: str
    type1: str
    type2: str


class PokemonAdmin(ModelView, model=Pokemon):
    page_size = 20
    icon = "fa-solid fa-spaghetti-monster-flying"
    column_searchable_list = [Pokemon.name]
    column_sortable_list = [Pokemon.name, Pokemon.classification, Pokemon.type1, Pokemon.type2]
    column_list = [
        Pokemon.pokedex_number,
        Pokemon.name,
        Pokemon.classification,
        Pokemon.type1,
        Pokemon.type2
    ]
