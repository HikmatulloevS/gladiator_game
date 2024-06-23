from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

characters = [
    {"id": 1, "name": f"Character 1", "strength": 0, "agility": 0, "stamina": 0, "level": 1, "availablePoints": 5},
    {"id": 2, "name": f"Character 2", "strength": 0, "agility": 0, "stamina": 0, "level": 1, "availablePoints": 5},
    {"id": 3, "name": f"Character 3", "strength": 0, "agility": 0, "stamina": 0, "level": 1, "availablePoints": 5}
]

lobbies = [
    {"id": 1, "players": []}
]


class Character(BaseModel):
    id: int = len(characters) + 1
    name: str = None
    strength: int = 0
    agility: int = 0
    stamina: int = 0
    level: int = 1
    availablePoints: int = 5


class Upgrade(BaseModel):
    strength: int = 0
    agility: int = 0
    stamina: int = 0


class Lobby(BaseModel):
    id: int = None
    players: list = []


def get_char_id(id: int):
    char = [char for char in characters if char.get("id") == id]
    if len(char) > 0:
        return char[0]
    return None


def get_lb_id(id: int):
    lobby = [lb for lb in lobbies if lb.get("id") == id]
    if len(lobby) > 0:
        return lobby[0]
    return None

@app.get("/")
async def check():
    return "checking"


@app.post("/api/characters")
async def create_character(character: Character):
    characters.append(character)
    return character


@app.get("/api/characters/{id}")
async def get_character(id: int):
    char = get_char_id(id)
    if char is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return char


@app.put("/api/characters/{id}/attributes")
async def adjust_character_attributes(id: int, upgrade: Upgrade):
    char = get_char_id(id)
    if char is None:
        raise HTTPException(status_code=404, detail="Character not found")
    amount_pt = upgrade.agility + upgrade.stamina + upgrade.strength
    if not amount_pt <= char["availablePoints"]:
        return {"response": "Not enough points"}

    #Обновление навыков
    char["strength"] += upgrade.strength
    char["agility"] += upgrade.agility
    char["stamina"] += upgrade.stamina
    char["availablePoints"] -= amount_pt

    return {"response": f"{char}"}


@app.post("/api/lobbies")
async def create_lobby():
    lobby = Lobby(id=len(lobbies) + 1)
    lobbies.append(lobby)
    return lobby


@app.post("/api/lobbies/{lobbyId}/join")
async def join_lobby(lobbyId: int, char_id: dict):
    #Поиск лобби
    lobby: Lobby = get_lb_id(lobbyId)
    if lobby is None:
        raise HTTPException(status_code=404, detail="Lobby not found")

    #Поиск персонажа
    character: Character = get_char_id(char_id["characterId"])
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    #Подключение игрока в лобби
    if character in lobby["players"]:
        raise HTTPException(status_code=404, detail="Character is already in lobby")
    lobby["players"].append(character)
    return lobby
