from fastapi import Depends
from sqlalchemy.orm import Session

from event_sourcing_example.database import get_db
from event_sourcing_example.example_data.event_models import ExampleDataEvent


class ExampleDataRepository:
    _db_session: Session

    def __init__(self, session: Session = Depends(get_db)):
        self._db_session = session


    def add_event(self, event: ExampleDataEvent) -> None:
        self._db_session.add(event)
        self._db_session.commit()
