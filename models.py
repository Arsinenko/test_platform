from typing import List, Optional

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Test(Base):
    __tablename__ = 'Test'

    subject = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, primary_key=True)

    Question: Mapped[List['Question']] = relationship(
        'Question', uselist=True, back_populates='Test_')


class Question(Base):
    __tablename__ = 'Question'

    content = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    id_test = mapped_column(ForeignKey('Test.id'))

    Test_: Mapped[Optional['Test']] = relationship(
        'Test', back_populates='Question')
    Answer: Mapped[List['Answer']] = relationship(
        'Answer', uselist=True, back_populates='Question_')


class Answer(Base):
    __tablename__ = 'Answer'
    __table_args__ = (
        CheckConstraint('right_answer in (1, 0) '),
    )

    content = mapped_column(Text, nullable=False)
    id_question = mapped_column(ForeignKey('Question.id'), nullable=False)
    id = mapped_column(Integer, primary_key=True)
    right_answer = mapped_column(Integer)

    Question_: Mapped['Question'] = relationship(
        'Question', back_populates='Answer')
