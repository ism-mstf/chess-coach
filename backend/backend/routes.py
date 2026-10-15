from fastapi import APIRouter, UploadFile, File, HTTPException
import chess.pgn
from ..models import Game, init_db, SessionLocal
from ..analysis import analyze_game
from sqlalchemy.orm import Session
import io

router = APIRouter()

@router.post('/import')
async def import_pgn(file: UploadFile = File(...)):
    if not file.filename.endswith('.pgn'):
        raise HTTPException(status_code=400, detail='Only PGN files are supported')
    content = await file.read()
    try:
        pgn_text = content.decode('utf-8')
    except Exception:
        raise HTTPException(status_code=400, detail='Could not decode PGN file')
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        raise HTTPException(status_code=400, detail='No valid game found in PGN')
    db = SessionLocal()
    g = Game.from_pgn(game, raw_pgn=pgn_text)
    db.add(g)
    db.commit()
    db.refresh(g)
    # Run synchronous analysis for MVP
    analyze_game(g.id)
    return {'game_id': g.id}
