from enum import Enum
from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Annotated
from database import Base, engine
from config import settings
import datetime

class Workload(Enum):
    fulltime = 'fulltime'
    parttime = 'parttime'

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime.datetime, 
                       mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, 
                       mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.now(datetime.timezone.utc))]

class WorkersORM(Base):
    __tablename__ = 'workers'
    id: Mapped[intpk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    resumes: Mapped[list["ResumesORM"]] = relationship(back_populates="worker")
    resumes_parttime: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersORM.id == ResumesORM.worker_id, ResumesORM.workload == 'parttime')")

class ResumesORM(Base):
    __tablename__ = 'resumes'
    id: Mapped[intpk]
    title: Mapped[str]
    compensation: Mapped[int]
    workload: Mapped[Workload]
    worker_id: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    worker: Mapped["WorkersORM"] = relationship(back_populates="resumes")