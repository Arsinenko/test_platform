from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas import CreateQuestionSchema
from services.question_services import (
    create,
    get_all,
    get_by_id,
    get_by_test_id,
    delete_question,
    update_question
)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/create_qestion")
async def create_question(model: CreateQuestionSchema, db: AsyncSession = Depends(get_db)):
    """Create new question"""
    return await create(model.content, model.id_test, db) 


@router.get("/get_by_id/{id}")
async def get_by_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """Get question by id """
    question =  await get_by_id(id, db)
    if not question:
        return HTTPException(status_code=404, detail="Question not found!")
    return question


@router.get("/all")
async def get_all_endpoint(db: AsyncSession = Depends(get_db)):
    """get all questions"""
    return await get_all(db)


@router.get("/get_by_test_id/{id}")
async def get_by_test_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """get questions by test id"""
    return await get_by_test_id(id, db)


@router.put("/update/{id}")
async def update_question_endpoint(id: int, content: str, db: AsyncSession = Depends(get_db)):
    """Update question content by id"""
    question = await update_question(id, content, db)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found!")
    return question



@router.delete("/delete_question/{id}")
async def delete_question_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    """delete_question question by id"""
    return await delete_question(id, db)