from typing import Optional

from sqlmodel import Field, SQLModel


class Pokemon(SQLModel, table=True):
    # __tablename__ = "pokemon"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    pokedex_number: int
    classification: str
    type1: str
    type2: str