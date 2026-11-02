from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class GameCreate(BaseModel):
    title: str
    genre: str
    players: int

class Game(BaseModel):
    id: int
    title: str
    genre: str
    players: int


games_db: List[Game] = [
    Game(id=1, title="Монополия", genre="Экономическая", players=4),
    Game(id=2, title="Каркассон", genre="Стратегия", players=5)
]

@app.get("/games", response_model=List[Game])
def get_all_games():

    return games_db

@app.post("/games", response_model=Game, status_code=201)
def create_game(game: GameCreate):
    new_id = max((g.id for g in games_db), default=0) + 1

    new_game = Game(
        id=new_id,
        title=game.title,
        genre=game.genre,
        players=game.players
    )
    games_db.append(new_game)

    return new_game

@app.put("/games/{game_id}", response_model=Game)
def update_game(game_id: int, updated_game: GameCreate):
    for index, game in enumerate(games_db):
        if game.id == game_id:
            new_game_data = Game(
                id=game_id,
                title=updated_game.title,
                genre=updated_game.genre,
                players=updated_game.players
            )
            games_db[index] = new_game_data
            return new_game_data

    raise HTTPException(status_code=404, detail="Игра с таким ID не найдена")

@app.delete("/games/{game_id}", response_model=Game)
def delete_game(game_id: int):
    for index, game in enumerate(games_db):
        if game.id == game_id:
            deleted_game = games_db.pop(index)
            return deleted_game

    raise HTTPException(status_code=404, detail="Игра с таким ID не найдена")