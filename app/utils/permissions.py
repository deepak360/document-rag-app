from sqlalchemy import select
from app.models.user import User
from app.models.permission import Permission, RolePermission
from sqlalchemy.ext.asyncio import AsyncSession

async def has_permission(user: User, feature: str, db: AsyncSession) -> bool:
    stmt = (
        select(Permission.id)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .where(RolePermission.role == user.role, Permission.feature == feature)
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar() is not None
