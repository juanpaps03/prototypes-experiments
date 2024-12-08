from event_sourcing_example.database import get_db
from event_sourcing_example.example_data.event_models import ExampleDataEvent



class ExampleDataRepository:

    def __init__(self):
        self._db_session = get_db()


    def add_event(self, event: ExampleDataEvent) -> None:
        self._db_session.add(event)
        self._db_session.commit()
