from app.db.sql import engine, Base
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)