import chess
import chess.engine
from .models import SessionLocal, Game, init_db

STOCKFISH_PATH = '/usr/local/bin/stockfish_16_x64_avx2'

init_db()


def analyze_game(game_id: int):
    db = SessionLocal()
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise ValueError('Game not found')
    pgn = chess.pgn.read_game(io.StringIO(game.raw_pgn))
    board = pgn.board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    node = pgn
    move_index = 0
    while node.variation(0) if node is not None and node.variations else False:
        try:
            move = node.variation(0).move
            board.push(move)
            # get evaluation after move
            info = engine.analyse(board, chess.engine.Limit(depth=12))
            cp = info.get('score').white().score(mate_score=100000)
            # TODO: store move info
            move_index += 1
            node = node.variation(0)
        except Exception:
            break
    engine.quit()
