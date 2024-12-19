from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from event_sourcing_example.settings import app_settings


engine = create_engine(app_settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()