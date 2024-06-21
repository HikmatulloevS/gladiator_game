from fastapi import FastAPI
from pydantic import BaseModel

characters = [
    {"id": 1, "name": f"Character 1", "strength": 0, "agility": 0, "stamina": 0, "level": 1, "availablePoints": 5},
    {"id": 2, "name": f"Character 2", "strength": 0, "agility": 0, "stamina": 0, "level": 1, "availablePoints": 5},
    {"id": 3, "name": f"Character 3", "strength": 0, "agility": 0, "stamina": 0, "level": 1, "availablePoints": 5}
]


class Character(BaseModel):
    name: str = None
    id: int = len(characters) + 1,
    strength: int = 0,
    agility: int = 0,
    stamina: int = 0,
    level: int = 1,
    availablePoints: int = 5


class Upgrade(BaseModel):
    strength: int = 0,
    agility: int = 0,
    stamina: int = 0


def get_id(id: int):
    char = [char for char in characters if char.get("id") == id]
    if len(char) > 0:
        return char[0]
    return None


app = FastAPI()


@app.get("/")
async def check():
    return f"checking"


@app.post("/api/characters")
async def create_character(character: Character):
    characters.append(character)
    return {"response": f"success \n{character}"}


@app.get("/api/characters/{id}")
async def get_character(id: int):
    char = get_id(id)
    if char is None:
        return {"response": "Character not found"}
    return char


@app.put("/api/characters/{id}/attributes")
async def adjust_character_attributes(id: int, upgrade: Upgrade):
    char = get_id(id)
    if char is None:
        return {"response": "Character not found"}
    amount_pt = upgrade.agility + upgrade.stamina + upgrade.strength
    if not amount_pt <= char["availablePoints"]:
        return {"response": "Not enough points"}
    char["strength"] += upgrade.strength
    char["agility"] += upgrade.agility
    char["stamina"] += upgrade.stamina
    char["availablePoints"] -= amount_pt

    return {"response": f"success \n{char}"}
