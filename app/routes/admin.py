from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.sql import get_db
from app.models.user import User
from app.schemas.user import UserOut
from app.core.deps import get_current_user

router = APIRouter()

def require_admin(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin only")
    return user

@router.get("/users", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()
