from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

from db import engine

Base = declarative_base()

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, autoincrement=True, primary_key=True)
    question = Column(String, nullable=False)
    valid_answer = Column(String, nullable=False)
    answer_2 = Column(String, nullable=False)
    answer_3 = Column(String, nullable=True)
    answer_4 = Column(String, nullable=True)


class QuizResult(Base):
    __tablename__ = "quiz_result"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

Base.metadata.create_all(engine)