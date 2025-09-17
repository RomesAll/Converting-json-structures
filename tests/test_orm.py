from sqlalchemy import text
from models import WorkersORM, ResumesORM
from database import Base, engine
from config import settings
import pytest

@pytest.fixture(scope='class', autouse=True)
def setup_db():
    assert settings.database.POSTGRES_MODE == 'TEST'
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function', autouse=True)
def setup_date_for_db():
    with engine.connect() as connect:
        connect.execute(text("INSERT INTO workers(first_name, last_name, phone, email) VALUES('Роман', 'Бобр', '+79021342953', 'rome@gmail.com')"))
        connect.execute(text("INSERT INTO workers(first_name, last_name, phone, email) VALUES('Никита', 'Бурбек', '890123234', 'nikit@gmail.com')"))
        connect.execute(text("INSERT INTO workers(first_name, last_name, phone, email) VALUES('Том', 'Форд', '+19021342953', 'tom@gmail.com')"))
        connect.execute(text("INSERT INTO workers(first_name, last_name, phone, email) VALUES('Гучи', '-', '+7234234235235', 'hi@gmail.com')"))
        connect.commit()

class TestORM:
    def test_select_data(self):
        with engine.connect() as conn:
            query = text("SELECT * FROM workers")
            result_query = conn.execute(query)
            assert len(result_query.all()) == 4