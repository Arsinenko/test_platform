from models import Question
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional


async def create(content: str, id_test: int, db: AsyncSession) -> Question:
    question = Question(content=content, id_test=id_test)
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question


async def get_by_id(question_id: int, db: AsyncSession) -> Optional[Question]:
    query = select(Question).where(Question.id == question_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_all(db: AsyncSession) -> List[Question]:
    query = select(Question)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_by_test_id(test_id: int, db: AsyncSession) -> List[Question]:
    query = select(Question).where(Question.id_test == test_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_question(question_id: int, content: str, db: AsyncSession) -> Optional[Question]:
    query = update(Question).where(Question.id == question_id).values(content=content).returning(Question)
    result = await db.execute(query)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_question(question_id: int, db: AsyncSession) -> bool:
    query = delete(Question).where(Question.id == question_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0