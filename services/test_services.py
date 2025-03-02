from models import Test
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_test(db: AsyncSession, subject: str) -> Test:
    """Create a new test entry."""
    test = Test(subject=subject)
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return test


async def get_test(db: AsyncSession, test_id: int) -> Test | None:
    """Get a test by ID."""
    query = select(Test).where(Test.id == test_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_all_tests(db: AsyncSession) -> list[Test]:
    """Get all tests."""
    query = select(Test)
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_test(db: AsyncSession, test_id: int, subject: str) -> Test | None:
    """Update a test by ID."""
    test = await get_test(db, test_id)
    if test:
        test.subject = subject
        await db.commit()
        await db.refresh(test)
    return test


async def delete_test(db: AsyncSession, test_id: int) -> bool:
    """Delete a test by ID."""
    test = await get_test(db, test_id)
    if test:
        await db.delete(test)
        await db.commit()
        return True
    return False


