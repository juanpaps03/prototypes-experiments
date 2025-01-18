from enum import StrEnum, Enum

from sqlalchemy import Column, Integer, create_engine, cast, literal, Enum as sqlEnum
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

engine = create_engine("postgresql://user:password@localhost:5432/test", echo=True, future=True)

class StatusEnum(StrEnum):
    Pending = "pending"
    Final = "final"

StatusType = sqlEnum(StatusEnum, values_callable=lambda obj: [e.lower() for e in obj])

class ExampleModel(Base):
    id: int = Column(Integer(), primary_key=True)
    status: StatusEnum | None = Column(StatusType, nullable=True)

    __tablename__ = "example"


def test_str_enum_python12_sqlalchemy_problem():

    with Session(engine) as session:
        data = session.query(
            ExampleModel
        ).filter(
            ExampleModel.status == StatusEnum.Final,
        ).all()

        print([d.__dict__ for d in data] if isinstance(data, list) else data.__dict__)

test_str_enum_python12_sqlalchemy_problem()