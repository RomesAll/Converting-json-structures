from config import settings
from database import engine, Base
from sqlalchemy import text
import pytest

@pytest.fixture(scope='class', autouse=True)
def create_test_table():
    assert settings.database.POSTGRES_MODE == 'TEST'
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('create_all')
    yield
    Base.metadata.drop_all(engine)
    print('drop_all')

class TestConnectionDB:
    def test_connect(self):
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 'hello world'"))
            assert res.all()[0][0] == 'hello world'

    def test_get_mode_db(self):
        assert settings.database.POSTGRES_MODE == 'TEST'