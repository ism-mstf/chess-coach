from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///./chess_coach.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    white = Column(String(100))
    black = Column(String(100))
    result = Column(String(10))
    raw_pgn = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def from_pgn(cls, game, raw_pgn=''):
        white = game.headers.get('White', 'White')
        black = game.headers.get('Black', 'Black')
        result = game.headers.get('Result', '*')
        return cls(white=white, black=black, result=result, raw_pgn=raw_pgn)


def init_db():
    Base.metadata.create_all(bind=engine)
