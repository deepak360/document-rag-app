from fastapi import APIRouter

from app.routes import auth, users, ingest, qa, select, admin, documents, qa

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])
router.include_router(documents.router, prefix="/document", tags=["document"])
router.include_router(qa.router, prefix="/qa", tags=["qa"])

# router.include_router(ingest.router, prefix="/ingest", tags=["Document Ingestion"])
# router.include_router(qa.router, prefix="/qa", tags=["Q&A"])
# router.include_router(select.router, prefix="/select-documents", tags=["Document Selection"])