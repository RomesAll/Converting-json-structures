from enum import Enum
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Annotated
from database import Base
import datetime


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at_base = Annotated[datetime.datetime, 
                       mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at_base = Annotated[datetime.datetime, 
                       mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)]


class WorkersORM(Base):
    __tablename__ = 'workers'
    id: Mapped[intpk]
    first_name: Mapped[str]
    last_name: Mapped[str] = None
    phone: Mapped[str] = None
    email: Mapped[str] = None
    created_at: Mapped[created_at_base]
    updated_at: Mapped[updated_at_base]

    resumes: Mapped[list["ResumesORM"]] = relationship(back_populates="worker")
    resumes_parttime: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersORM.id == ResumesORM.worker_id, ResumesORM.workload == 'parttime')")

    def update_attrs(self, new_data):

        if self.first_name != new_data.first_name and new_data.first_name:
            self.first_name = new_data.first_name

        if self.last_name != new_data.last_name and new_data.last_name:
            self.last_name = new_data.last_name

        if self.phone != new_data.phone and new_data.phone:
            self.phone = new_data.phone

        if self.email != new_data.email and new_data.email:
            self.email = new_data.email

        if self.created_at != new_data.created_at and new_data.created_at:
            self.created_at = new_data.created_at

        if self.updated_at != new_data.updated_at and new_data.updated_at:
            self.updated_at = new_data.updated_at

class Workload(Enum):
    fulltime = "fulltime"
    parttime = "parttime"

class ResumesORM(Base):
    __tablename__ = 'resumes'
    id: Mapped[intpk]
    title: Mapped[str]
    compensation: Mapped[int]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at_base]
    updated_at: Mapped[updated_at_base]
    worker: Mapped["WorkersORM"] = relationship(back_populates="resumes")

    def update_attrs(self, new_data):
        self.title = new_data.title if new_data.title else self.title
        self.compensation = new_data.compensation if new_data.compensation else self.compensation
        self.workload = new_data.workload if new_data.workload else self.workload
        self.worker_id = new_data.worker_id if new_data.worker_id else self.worker_id