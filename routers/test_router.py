from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import shutil

from db import get_db
from models import Test
from services.test_services import (
    create_test,
    get_test,
    get_all_tests,
    update_test,
    delete_test,
)
from services.parse_docx import parse_file

router = APIRouter(
    prefix="/tests",
    tags=["tests"]
)


@router.post("/upload_file")
async def upload_file(file: UploadFile):
    try: 
        with open(f"{file.filename}", "wb") as content:
            shutil.copyfileobj(file.file, content)
        return {"message": "success"}
    except Exception as ex:
        raise HTTPException(500, detail=str(ex))
    


@router.post("/create")
async def create_test_endpoint(subject: str, db: AsyncSession = Depends(get_db)):
    """Create a new test."""
    return await create_test(db, subject)


@router.get("/get_gest/{test_id}")
async def get_test_endpoint(test_id: int, db: AsyncSession = Depends(get_db)):
    """Get a test by ID."""
    test = await get_test(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.get("/")
async def get_all_tests_endpoint(db: AsyncSession = Depends(get_db)):
    """Get all tests."""
    return await get_all_tests(db)


@router.put("/{test_id}")
async def update_test_endpoint(test_id: int, subject: str, db: AsyncSession = Depends(get_db)):
    """Update a test by ID."""
    test = await update_test(db, test_id, subject)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.delete("/{test_id}")
async def delete_test_endpoint(test_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a test by ID."""
    success = await delete_test(db, test_id)
    if not success:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": "Test deleted successfully"} 