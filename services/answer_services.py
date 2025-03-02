from models import Answer
from sqlalchemy.ext.asyncio import AsyncSession

async def create_answer(content: str,  right_answer: bool, db: AsyncSession):
    answer = Answer()